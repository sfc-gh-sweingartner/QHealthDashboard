import streamlit as st
import snowflake.connector
import pandas as pd
from typing import Optional, Dict, Any, Union
import time
import tomli
from snowflake.snowpark.context import get_active_session

@st.cache_resource
def get_snowflake_connection() -> Optional[Union[snowflake.connector.SnowflakeConnection, object]]:
    """
    Create and cache Snowflake connection using hybrid approach:
    1. First try to get active session (for Streamlit in Snowflake)
    2. Fall back to local config file
    Returns None if connection fails.
    """
    # First try to get active session (for Streamlit in Snowflake)
    try:
        session = get_active_session()
        if session:
            # No need to set database context in Snowflake - use fully qualified names
            st.success("✅ Connected via Streamlit in Snowflake session")
            return session
    except Exception:
        # If get_active_session fails, continue to local connection
        pass
            
    # Try local connection using config file
    try:
        with open('/Users/sweingartner/.snowflake/config.toml', 'rb') as f:
            config = tomli.load(f)
        
        # Get the default connection name
        default_conn = config.get('default_connection_name')
        if not default_conn:
            st.error("No default connection specified in config.toml")
            return None
            
        # Get the connection configuration for the default connection
        conn_params = config.get('connections', {}).get(default_conn)
        if not conn_params:
            st.error(f"Connection '{default_conn}' not found in config.toml")
            return None
        
        # Create a connection
        conn = snowflake.connector.connect(**conn_params)
        
        # Test connection without setting context (use fully qualified names)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT CURRENT_VERSION()")
            cursor.fetchone()
            st.success("✅ Connected via local Snowflake config")
        except Exception as e:
            st.warning(f"Connection test failed: {str(e)}")
        finally:
            cursor.close()
        
        return conn
        
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None

def test_connection(conn: Union[snowflake.connector.SnowflakeConnection, object]) -> bool:
    """Test if the Snowflake connection is working"""
    try:
        # Handle both session and connection types
        if hasattr(conn, 'sql'):  # Snowpark session
            result = conn.sql("SELECT CURRENT_VERSION()").collect()
            return len(result) > 0
        else:  # Regular connection
            cursor = conn.cursor()
            cursor.execute("SELECT CURRENT_VERSION()")
            result = cursor.fetchone()
            cursor.close()
            return result is not None
    except:
        return False

@st.cache_data(ttl=300)  # Cache for 5 minutes
def execute_query(_conn: Union[snowflake.connector.SnowflakeConnection, object], query: str, params: Optional[Dict] = None) -> pd.DataFrame:
    """
    Execute SQL query and return results as pandas DataFrame.
    Cached for 5 minutes to improve performance.
    """
    start_time = time.time()
    
    try:
        # Handle both session and connection types
        if hasattr(_conn, 'sql'):  # Snowpark session
            if params:
                # For Snowpark sessions, parameters need to be handled differently
                # This is a simplified approach - you may need to adjust based on your specific needs
                df = _conn.sql(query).to_pandas()
            else:
                df = _conn.sql(query).to_pandas()
        else:  # Regular connection
            cursor = _conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Fetch results and column names
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            # Create DataFrame
            df = pd.DataFrame(results, columns=columns)
            
            cursor.close()
        
        # Log performance
        execution_time = time.time() - start_time
        if execution_time > 3:
            st.warning(f"⚠️ Query took {execution_time:.1f}s (target: <3s)")
        else:
            st.success(f"✅ Query executed in {execution_time:.1f}s")
        
        return df
        
    except Exception as e:
        st.error(f"Query execution failed: {str(e)}")
        return pd.DataFrame()

def get_database_info(_conn: Union[snowflake.connector.SnowflakeConnection, object]) -> Dict[str, Any]:
    """Get basic database information for monitoring"""
    try:
        info = {}
        
        # Get record counts for main tables
        queries = {
            'checkup_lite_records': "SELECT COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS",
            'dose_records': "SELECT COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS", 
            'patients': "SELECT COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_PATIENTS",
            'providers': "SELECT COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_PROVIDERS"
        }
        
        for key, query in queries.items():
            try:
                df = execute_query(_conn, query)
                info[key] = df.iloc[0, 0] if not df.empty else 0
            except:
                info[key] = 0
        
        return info
        
    except Exception as e:
        st.error(f"Failed to get database info: {str(e)}")
        return {}

# Connection helper for pages
def ensure_connection():
    """Ensure Snowflake connection is available, redirect to main page if not"""
    if 'snowflake_connection' not in st.session_state or st.session_state.snowflake_connection is None:
        st.error("❌ No Snowflake connection available. Please connect on the main page first.")
        st.stop()
    
    return st.session_state.snowflake_connection

# Query performance monitoring
@st.cache_data(ttl=60)  # Cache for 1 minute
def get_query_performance_stats(_conn: Union[snowflake.connector.SnowflakeConnection, object]) -> Dict[str, float]:
    """Get query performance statistics"""
    try:
        query = """
        SELECT 
            AVG(EXECUTION_TIME) as avg_execution_time,
            MAX(EXECUTION_TIME) as max_execution_time,
            COUNT(*) as query_count
        FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
        WHERE START_TIME >= CURRENT_TIMESTAMP - INTERVAL '1 HOUR'
        AND QUERY_TYPE = 'SELECT'
        """
        
        df = execute_query(_conn, query)
        if not df.empty:
            return {
                'avg_time': df['AVG_EXECUTION_TIME'].iloc[0] / 1000,  # Convert to seconds
                'max_time': df['MAX_EXECUTION_TIME'].iloc[0] / 1000,
                'query_count': df['QUERY_COUNT'].iloc[0]
            }
    except:
        pass
    
    return {'avg_time': 0, 'max_time': 0, 'query_count': 0}