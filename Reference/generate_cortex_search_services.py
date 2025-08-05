#!/usr/bin/env python3
"""
Generic Cortex Search Services Generator for Snowflake Semantic Models

This script automatically adds cortex_search_service entries to YAML semantic models
based on Cortex Search Services defined in SQL files. It follows Snowflake best 
practices by only adding search services to dimension fields.

Usage:
    python generate_cortex_search_services.py [yaml_file] [sql_file]
    
    If no arguments provided, uses default files:
    - syntheaSI1.yaml (for YAML)
    - create_synthea_cortex_search_services.sql (for SQL)

Author: Auto-generated for Synthea Healthcare Text2SQL package
"""

import re
import yaml
import sys
import os
from typing import Dict, Tuple, Optional

def extract_search_services(sql_file: str) -> Dict[str, str]:
    """
    Extract search service mappings from SQL file.
    
    Args:
        sql_file: Path to SQL file containing CREATE CORTEX SEARCH SERVICE statements
        
    Returns:
        Dict mapping 'TABLE_COLUMN' to 'search_service_name'
        
    Raises:
        FileNotFoundError: If SQL file doesn't exist
        ValueError: If no search services found in SQL file
    """
    if not os.path.exists(sql_file):
        raise FileNotFoundError(f"SQL file not found: {sql_file}")
        
    services = {}
    
    with open(sql_file, 'r') as f:
        content = f.read()
    
    # Pattern to match: CREATE OR REPLACE CORTEX SEARCH SERVICE servicename
    # Supports various naming patterns:
    # - Search_Synthea_Table_Column
    # - Search_Table_Column  
    # - TABLE_COLUMN_SEARCH
    patterns = [
        r'CREATE\s+(?:OR\s+REPLACE\s+)?CORTEX\s+SEARCH\s+SERVICE\s+(Search_(?:\w+_)?(\w+)_(\w+))',
        r'CREATE\s+(?:OR\s+REPLACE\s+)?CORTEX\s+SEARCH\s+SERVICE\s+((\w+)_(\w+)_SEARCH)',
        r'CREATE\s+(?:OR\s+REPLACE\s+)?CORTEX\s+SEARCH\s+SERVICE\s+((\w+)_(\w+))'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if len(match) >= 3:
                service_name, table_name, column_name = match[0], match[1], match[2]
                key = f"{table_name.upper()}_{column_name.upper()}"
                services[key] = service_name
                print(f"Found service: {table_name}.{column_name} -> {service_name}")
    
    if not services:
        raise ValueError(f"No Cortex Search Services found in {sql_file}. Check the SQL syntax.")
    
    return services

def validate_yaml_structure(data: dict) -> bool:
    """
    Validate that the YAML has the expected semantic model structure.
    
    Args:
        data: Parsed YAML data
        
    Returns:
        True if valid structure, False otherwise
    """
    if not isinstance(data, dict):
        return False
        
    if 'tables' not in data:
        print("Warning: No 'tables' section found in YAML. This might not be a semantic model.")
        return False
        
    tables = data['tables']
    if not isinstance(tables, list) or len(tables) == 0:
        print("Warning: 'tables' section is empty or not a list.")
        return False
        
    # Check that at least one table has dimensions
    has_dimensions = any(
        isinstance(table, dict) and 'dimensions' in table 
        for table in tables
    )
    
    if not has_dimensions:
        print("Warning: No tables with 'dimensions' found. This script only adds search services to dimensions.")
        return False
        
    return True

def backup_file(file_path: str) -> str:
    """
    Create a backup of the original file.
    
    Args:
        file_path: Path to file to backup
        
    Returns:
        Path to backup file
    """
    backup_path = f"{file_path}.backup"
    counter = 1
    
    # Find a unique backup filename
    while os.path.exists(backup_path):
        backup_path = f"{file_path}.backup.{counter}"
        counter += 1
    
    with open(file_path, 'r') as original:
        with open(backup_path, 'w') as backup:
            backup.write(original.read())
    
    print(f"Created backup: {backup_path}")
    return backup_path

def add_search_services_to_yaml(yaml_file: str, services: Dict[str, str], create_backup: bool = True) -> Tuple[int, int]:
    """
    Add cortex search services to YAML file dimensions while preserving formatting.
    
    Args:
        yaml_file: Path to YAML semantic model file
        services: Dict mapping table_column to search service names
        create_backup: Whether to create a backup before modifying
        
    Returns:
        Tuple of (changes_made, total_dimensions_processed)
        
    Raises:
        FileNotFoundError: If YAML file doesn't exist
        ValueError: If YAML structure is invalid
    """
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"YAML file not found: {yaml_file}")
    
    # Create backup if requested
    if create_backup:
        backup_file(yaml_file)
    
    # Read and validate file
    with open(yaml_file, 'r') as f:
        content = f.read()
    
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax in {yaml_file}: {e}")
    
    if not validate_yaml_structure(data):
        raise ValueError(f"YAML file {yaml_file} doesn't appear to be a valid semantic model")
    
    changes_made = 0
    dimensions_processed = 0
    
    # Process each table
    for table in data.get('tables', []):
        table_name = table.get('name', '').upper()
        
        # Only process dimensions (following Snowflake best practices)
        for dimension in table.get('dimensions', []):
            dimensions_processed += 1
            column_name = dimension.get('name', '').upper()
            key = f"{table_name}_{column_name}"
            
            if key in services:
                # Use regex to find and modify this specific dimension in the text
                dimension_pattern = rf'(  - name: {re.escape(dimension.get("name", ""))}\n(?:.*\n)*?    sample_values:\n(?:.*\n)*?)(?=  - name:|time_dimensions:|facts:|metrics:|primary_key:|relationships:|^- name:|\Z)'
                
                match = re.search(dimension_pattern, content, re.MULTILINE)
                if match:
                    dimension_block = match.group(1)
                    
                    # Check if cortex_search_service already exists
                    if 'cortex_search_service:' not in dimension_block:
                        # Find the end of the last sample value
                        sample_values_end = dimension_block.rfind('    - ')
                        if sample_values_end != -1:
                            next_newline = dimension_block.find('\n', sample_values_end)
                            if next_newline != -1:
                                # Insert cortex_search_service after sample_values
                                search_service_text = f"    cortex_search_service:\n      service: {services[key]}\n"
                                new_dimension_block = dimension_block[:next_newline+1] + search_service_text + dimension_block[next_newline+1:]
                                
                                # Replace in content
                                content = content.replace(dimension_block, new_dimension_block)
                                changes_made += 1
                                print(f"✓ Added search service for {table_name}.{column_name}")
                    else:
                        print(f"⚠ Search service already exists for {table_name}.{column_name}")
    
    # Write back to file
    with open(yaml_file, 'w') as f:
        f.write(content)
    
    return changes_made, dimensions_processed

def main():
    """Main function with command-line argument handling."""
    # Default file names
    default_yaml = 'syntheaSI1.yaml'
    default_sql = 'create_synthea_cortex_search_services.sql'
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        yaml_file = default_yaml
        sql_file = default_sql
        print(f"Using default files: {yaml_file}, {sql_file}")
    elif len(sys.argv) == 3:
        yaml_file = sys.argv[1]
        sql_file = sys.argv[2]
        print(f"Using specified files: {yaml_file}, {sql_file}")
    else:
        print("Usage: python generate_cortex_search_services.py [yaml_file] [sql_file]")
        print("   or: python generate_cortex_search_services.py  (uses default files)")
        sys.exit(1)
    
    try:
        print(f"\n🔍 Extracting search services from {sql_file}...")
        services = extract_search_services(sql_file)
        print(f"✓ Found {len(services)} search services")
        
        print(f"\n📝 Updating YAML file {yaml_file}...")
        changes_made, dimensions_processed = add_search_services_to_yaml(yaml_file, services)
        
        print(f"\n📊 Summary:")
        print(f"   • Dimensions processed: {dimensions_processed}")
        print(f"   • Search services added: {changes_made}")
        print(f"   • Backup created: {yaml_file}.backup")
        
        if changes_made > 0:
            print(f"\n✅ Successfully updated {yaml_file}!")
            print("Your semantic model now has enhanced fuzzy search capabilities.")
        else:
            print(f"\nℹ️  No changes made to {yaml_file}")
            print("This could mean search services were already configured or no matching columns found.")
            
    except (FileNotFoundError, ValueError) as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Please check your input files and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 