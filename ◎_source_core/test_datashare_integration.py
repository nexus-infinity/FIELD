#!/usr/bin/env python3
"""
Test script for Datashare integration
"""

import asyncio
import httpx
import json

async def test_datashare_connection():
    """Test connection to Datashare API"""
    
    base_url = "http://localhost:9630"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Test basic connectivity
        try:
            response = await client.get(f"{base_url}/")
            print(f"✅ Datashare web interface accessible (status: {response.status_code})")
        except Exception as e:
            print(f"❌ Failed to connect to Datashare web interface: {e}")
            return
            
        # Test API endpoints
        endpoints_to_test = [
            "/api/projects",
            "/api/settings/public",
            "/api/index/search",
        ]
        
        for endpoint in endpoints_to_test:
            try:
                response = await client.get(f"{base_url}{endpoint}")
                if response.status_code == 200:
                    content = response.json()
                    print(f"✅ {endpoint} - Status: {response.status_code}")
                    if isinstance(content, dict) and content.get('error') == '':
                        print(f"   Empty response (likely no data)")
                    else:
                        print(f"   Response: {json.dumps(content, indent=2)[:200]}...")
                else:
                    print(f"⚠️  {endpoint} - Status: {response.status_code}")
                    print(f"   Response: {response.text[:200]}...")
                    
            except Exception as e:
                print(f"❌ Failed to test {endpoint}: {e}")
                
        # Test search functionality
        try:
            response = await client.get(f"{base_url}/api/index/search", params={"q": "*"})
            print(f"✅ Search API accessible (status: {response.status_code})")
            content = response.json()
            if isinstance(content, dict):
                print(f"   Search results: {json.dumps(content, indent=2)[:300]}...")
        except Exception as e:
            print(f"❌ Search test failed: {e}")

if __name__ == "__main__":
    print("🔍 Testing Datashare Integration...")
    print("=" * 50)
    asyncio.run(test_datashare_connection())
    print("=" * 50)
    print("✨ Test complete!")
    print("\nNext steps:")
    print("1. Add documents to Datashare via the web interface")
    print("2. Test the MCP bridge with actual data")
    print("3. Configure external data sources")