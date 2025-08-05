#!/usr/bin/env python3
"""
Script to add cortex search services ONLY to dimension fields in quaildashboard.yaml 
as per Snowflake Cortex Analyst specification
"""

import re
import yaml
from typing import Dict

def extract_search_services(sql_file: str) -> Dict[str, str]:
    """
    Extract search service mappings from SQL file.
    Returns dict mapping 'table_column' to 'search_service_name'
    """
    services = {}
    
    with open(sql_file, 'r') as f:
        content = f.read()
    
    # Find all CREATE OR REPLACE CORTEX SEARCH SERVICE statements
    # Pattern matches: Search_Quail_TableName_ColumnName
    pattern = r'CREATE OR REPLACE CORTEX SEARCH SERVICE (Search_Quail_(\w+)_(\w+))'
    matches = re.findall(pattern, content)
    
    for service_name, table_name, column_name in matches:
        # Map table_column to service name
        key = f"{table_name.upper()}_{column_name.upper()}"
        services[key] = service_name
        print(f"Found service: {table_name}.{column_name} -> {service_name}")
    
    return services

def add_search_services_to_dimensions_only(yaml_file: str, services: Dict[str, str]) -> None:
    """
    Add cortex search services ONLY to dimension fields, preserving YAML structure
    """
    # Read the file as text to preserve formatting
    with open(yaml_file, 'r') as f:
        content = f.read()
    
    # Also parse as YAML to understand structure
    data = yaml.safe_load(content)
    
    changes_made = 0
    
    # Process each table
    for table in data.get('tables', []):
        table_name = table.get('name', '').upper()
        
        # Only process dimensions, not facts, time_dimensions, or metrics
        for dimension in table.get('dimensions', []):
            column_name = dimension.get('name', '').upper()
            key = f"{table_name}_{column_name}"
            
            if key in services:
                # Use text replacement to add cortex_search_service while preserving formatting
                # Look for this specific dimension definition - adjust for actual 6-space indentation
                dimension_pattern = rf'(      - name: {re.escape(column_name)}\n(?:.*\n)*?)(?=      - name:|    time_dimensions:|    facts:|    metrics:|    primary_key:|relationships:|^  - name:|\Z)'
                
                match = re.search(dimension_pattern, content, re.MULTILINE)
                if match:
                    dimension_block = match.group(1)
                    
                    # Check if cortex_search_service already exists
                    if 'cortex_search_service:' not in dimension_block:
                        # Find the end of the last synonyms section
                        # Look for the last line that starts with "          - " (synonym item)
                        lines = dimension_block.split('\n')
                        insert_index = -1
                        
                        # Find the last synonym line
                        for i in range(len(lines) - 1, -1, -1):
                            if '          - ' in lines[i] and lines[i].strip():
                                insert_index = i
                                break
                        
                        if insert_index != -1:
                            # Insert cortex_search_service after the last synonym
                            search_service_text = f"        cortex_search_service:\n          service: {services[key]}"
                            lines.insert(insert_index + 1, search_service_text)
                            new_dimension_block = '\n'.join(lines)
                            
                            # Replace in content
                            content = content.replace(dimension_block, new_dimension_block)
                            changes_made += 1
                            print(f"Added search service for {table_name}.{column_name} (dimension only)")
    
    # Write back to file
    with open(yaml_file, 'w') as f:
        f.write(content)
    
    print(f"\nTotal changes made to dimensions: {changes_made}")

def main():
    sql_file = 'create_quaildashboard_cortex_search_services.sql'
    yaml_file = 'quaildashboard.yaml'
    
    print("Extracting search services from SQL file...")
    services = extract_search_services(sql_file)
    print(f"Found {len(services)} search services")
    
    print("\nAdding cortex_search_service ONLY to dimension fields...")
    add_search_services_to_dimensions_only(yaml_file, services)
    
    print("Done! Only dimension fields now have cortex_search_service entries.")

if __name__ == "__main__":
    main()