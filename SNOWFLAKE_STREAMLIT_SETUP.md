# Streamlit in Snowflake Setup Guide

## Required Libraries to Import

To make your Quantium Healthcare Analytics Platform work properly in Streamlit in Snowflake, you need to import these specific libraries through the Snowflake Streamlit UI:

### Core Required Libraries
1. **pandas** ✅ (you already have this)
2. **plotly** ✅ (you already have this)
3. **numpy** - **REQUIRED** (for data processing)
4. **altair** - **RECOMMENDED** (backup visualization)
5. **snowflake-snowpark-python** - **REQUIRED** (for Snowpark functionality)

### Optional but Recommended
6. **scipy** - for advanced statistical functions
7. **scikit-learn** - if using any ML features

## How to Import Libraries in Snowflake Streamlit

1. Open your Streamlit app in Snowflake
2. Go to the **Packages** menu at the top
3. Search for each library name
4. Click **Add** for each required library
5. **Restart your session** after adding all libraries

## Common Issues and Solutions

### Issue 1: Quick Data Overview Shows No Data
**Problem**: Connection not properly established
**Solution**: The app now uses real Snowflake queries instead of hardcoded data

### Issue 2: Treemap Shows Single Color
**Problem**: Color scale compatibility with Snowflake environment
**Solution**: Updated to use 'Viridis' color scale with better borders and labels

### Issue 3: ModuleNotFoundError for 'statsmodels'
**Problem**: statsmodels not available in Snowflake Anaconda channel
**Solutions**:
- **Option A**: Replace statsmodels functionality with scipy/numpy equivalents
- **Option B**: Use Snowflake's built-in statistical functions
- **Option C**: Upload statsmodels as a custom package (advanced)

### Issue 4: Performance Differences
**Problem**: Slower loading in Snowflake environment
**Solutions**:
- Add caching decorators: `@st.cache_data`
- Optimize queries to reduce data transfer
- Use Snowflake's native aggregation functions

## Library Alternatives for Snowflake

| Local Library | Snowflake Alternative | Purpose |
|--------------|---------------------|---------|
| statsmodels | scipy.stats + numpy | Statistical analysis |
| seaborn | plotly + altair | Data visualization |
| matplotlib | plotly | Static plots |
| custom packages | Upload to stage | Custom functionality |

## Testing Your Setup

1. **Deploy your updated code** to Snowflake Streamlit
2. **Import all required libraries** through the UI
3. **Test each page** to ensure functionality
4. **Check the logs** for any remaining import errors

## Updated Code Changes

### ✅ Fixed Issues:
- **Quick Data Overview**: Now uses real Snowflake data queries
- **Treemap Colors**: Improved color scale and border definition
- **Error Handling**: Better error messages and fallbacks

### 🔧 Code Improvements:
- Real-time data fetching from Snowflake tables
- Enhanced visualization compatibility
- Better error handling and user feedback

## Next Steps

1. **Test locally first** to ensure changes work
2. **Push to git repository**
3. **Deploy to Snowflake Streamlit**
4. **Import required libraries**
5. **Verify all functionality**

Remember: The visualization pages will work locally but may have limitations in Snowflake due to library restrictions. The core functionality (dose.py, checkup_lite.py) should work in both environments.