#!/usr/bin/env python3
"""
Sacred Trinity Agent Runner - Response Collection System
Automated response collection from FastAPI:8000, Flask:5000, Gradio:7860

Implements comprehensive Sacred Trinity testing with:
- FastAPI Quantum Conduit interaction
- Flask Glyph Weaver dashboard testing  
- Gradio Truth Mirror ethical processing
- Cross-component integration verification
"""

import os
import json
import asyncio
import aiohttp
import logging
import websockets
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SacredTrinityAgentRunner:
    """🤖 Automated response collection for Sacred Trinity evaluation"""
    
    def __init__(self):
        self.trinity_endpoints = {
            "fastapi": "http://localhost:8000",
            "flask": "http://localhost:5000", 
            "gradio": "http://localhost:7860"
        }
        self.session = None
        self.collected_responses = []
        self.health_status = {}
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def run_comprehensive_collection(self, test_queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run comprehensive response collection across Sacred Trinity"""
        logger.info("🌌 Initiating Sacred Trinity Response Collection...")
        
        # First check health of all components
        await self.check_trinity_health()
        
        # Collect responses for each test query
        for query_data in test_queries:
            try:
                response_data = await self.collect_component_response(query_data)
                self.collected_responses.append(response_data)
                
                # Add small delay between requests
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Failed to collect response for {query_data.get('test_id', 'unknown')}: {e}")
                # Add error response to maintain dataset consistency
                error_response = self._create_error_response(query_data, str(e))
                self.collected_responses.append(error_response)
        
        logger.info(f"✅ Collected {len(self.collected_responses)} responses from Sacred Trinity")
        return self.collected_responses
    
    async def check_trinity_health(self) -> Dict[str, bool]:
        """Check health status of all Sacred Trinity components"""
        logger.info("🔍 Checking Sacred Trinity health status...")
        
        health_checks = {
            "fastapi": self._check_fastapi_health(),
            "flask": self._check_flask_health(),
            "gradio": self._check_gradio_health()
        }
        
        # Run health checks concurrently
        for component, health_coro in health_checks.items():
            try:
                is_healthy = await health_coro
                self.health_status[component] = is_healthy
                status_emoji = "✅" if is_healthy else "❌"
                logger.info(f"{status_emoji} {component.upper()}: {'Healthy' if is_healthy else 'Unavailable'}")
            except Exception as e:
                self.health_status[component] = False
                logger.warning(f"❌ {component.upper()}: Health check failed - {e}")
        
        return self.health_status
    
    async def _check_fastapi_health(self) -> bool:
        """Check FastAPI Quantum Conduit health"""
        try:
            async with self.session.get(f"{self.trinity_endpoints['fastapi']}/", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("status") == "healthy"
                return False
        except Exception as e:
            logger.debug(f"FastAPI health check failed: {e}")
            return False
    
    async def _check_flask_health(self) -> bool:
        """Check Flask Glyph Weaver health"""
        try:
            async with self.session.get(f"{self.trinity_endpoints['flask']}/health", timeout=10) as response:
                if response.status == 200:
                    # Flask health endpoint might return HTML or JSON
                    content_type = response.headers.get('content-type', '')
                    if 'application/json' in content_type:
                        data = await response.json()
                        return data.get("status") == "healthy"
                    else:
                        # Check if HTML contains health indicators
                        html_content = await response.text()
                        return "healthy" in html_content.lower() or "pi forge" in html_content.lower()
                return False
        except Exception as e:
            logger.debug(f"Flask health check failed: {e}")
            return False
    
    async def _check_gradio_health(self) -> bool:
        """Check Gradio Truth Mirror health"""
        try:
            async with self.session.get(f"{self.trinity_endpoints['gradio']}/", timeout=10) as response:
                # Gradio typically returns 200 with HTML interface
                return response.status == 200
        except Exception as e:
            logger.debug(f"Gradio health check failed: {e}")
            return False
    
    async def collect_component_response(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect response from appropriate Sacred Trinity component"""
        component = query_data.get("component", "unknown")
        query = query_data.get("query", "")
        
        logger.info(f"📡 Collecting response from {component.upper()} for: {query[:50]}...")
        
        if component == "fastapi":
            response = await self._collect_fastapi_response(query_data)
        elif component == "flask": 
            response = await self._collect_flask_response(query_data)
        elif component == "gradio":
            response = await self._collect_gradio_response(query_data)
        elif component == "integration":
            response = await self._collect_integration_response(query_data)
        else:
            response = {"error": f"Unknown component: {component}", "status": "failed"}
        
        # Enrich response with collection metadata
        enriched_response = {
            **query_data,  # Include original query data
            "response": response.get("response", "No response available"),
            "response_metadata": {
                "collection_timestamp": datetime.utcnow().isoformat(),
                "component_status": self.health_status.get(component, False),
                "response_status": response.get("status", "unknown"),
                "response_time_ms": response.get("response_time_ms", 0),
                "error": response.get("error")
            }\n        }\n        \n        return enriched_response\n    \n    async def _collect_fastapi_response(self, query_data: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"Collect response from FastAPI Quantum Conduit\"\"\"\n        start_time = asyncio.get_event_loop().time()\n        \n        try:\n            # Test different FastAPI endpoints based on query focus\n            evaluation_focus = query_data.get(\"evaluation_focus\", \"general\")\n            \n            if \"authentication\" in evaluation_focus:\n                endpoint = \"/\"\n            elif \"websocket\" in evaluation_focus or \"consciousness\" in evaluation_focus:\n                return await self._test_websocket_connection()\n            elif \"database\" in evaluation_focus:\n                endpoint = \"/users/me\"  # Protected endpoint requiring auth\n            else:\n                endpoint = \"/\"  # Default health endpoint\n            \n            url = f\"{self.trinity_endpoints['fastapi']}{endpoint}\"\n            \n            async with self.session.get(url, timeout=15) as response:\n                response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n                \n                if response.status == 200:\n                    try:\n                        data = await response.json()\n                        return {\n                            \"response\": f\"FastAPI response: {json.dumps(data, indent=2)}\",\n                            \"status\": \"success\",\n                            \"response_time_ms\": response_time\n                        }\n                    except:\n                        text_data = await response.text()\n                        return {\n                            \"response\": f\"FastAPI response: {text_data[:500]}...\",\n                            \"status\": \"success\", \n                            \"response_time_ms\": response_time\n                        }\n                else:\n                    return {\n                        \"response\": f\"FastAPI returned status {response.status}\",\n                        \"status\": \"error\",\n                        \"response_time_ms\": response_time\n                    }\n                    \n        except Exception as e:\n            response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n            return {\n                \"response\": f\"FastAPI connection failed: {str(e)}\",\n                \"status\": \"failed\",\n                \"response_time_ms\": response_time,\n                \"error\": str(e)\n            }\n    \n    async def _test_websocket_connection(self) -> Dict[str, Any]:\n        \"\"\"Test WebSocket consciousness streaming\"\"\"\n        start_time = asyncio.get_event_loop().time()\n        \n        try:\n            ws_url = \"ws://localhost:8000/ws/collective-insight\"\n            \n            async with websockets.connect(ws_url, timeout=10) as websocket:\n                # Send test message\n                test_message = {\"type\": \"test\", \"message\": \"Sacred Trinity evaluation test\"}\n                await websocket.send(json.dumps(test_message))\n                \n                # Wait for response\n                response = await asyncio.wait_for(websocket.recv(), timeout=5)\n                response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n                \n                return {\n                    \"response\": f\"WebSocket connection successful: {response}\",\n                    \"status\": \"success\",\n                    \"response_time_ms\": response_time\n                }\n                \n        except Exception as e:\n            response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n            return {\n                \"response\": f\"WebSocket connection failed: {str(e)}\",\n                \"status\": \"failed\",\n                \"response_time_ms\": response_time,\n                \"error\": str(e)\n            }\n    \n    async def _collect_flask_response(self, query_data: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"Collect response from Flask Glyph Weaver\"\"\"\n        start_time = asyncio.get_event_loop().time()\n        \n        try:\n            evaluation_focus = query_data.get(\"evaluation_focus\", \"general\")\n            \n            if \"dashboard\" in evaluation_focus or \"visualization\" in evaluation_focus:\n                endpoint = \"/resonance-dashboard\"\n            elif \"quantum_processing\" in evaluation_focus:\n                endpoint = \"/resonate/test_hash_123\"\n            else:\n                endpoint = \"/health\"\n            \n            url = f\"{self.trinity_endpoints['flask']}{endpoint}\"\n            \n            async with self.session.get(url, timeout=15) as response:\n                response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n                \n                if response.status == 200:\n                    content_type = response.headers.get('content-type', '')\n                    \n                    if 'application/json' in content_type:\n                        data = await response.json()\n                        return {\n                            \"response\": f\"Flask dashboard data: {json.dumps(data, indent=2)[:500]}...\",\n                            \"status\": \"success\",\n                            \"response_time_ms\": response_time\n                        }\n                    else:\n                        html_content = await response.text()\n                        # Extract meaningful content from HTML\n                        response_summary = self._extract_flask_content(html_content)\n                        return {\n                            \"response\": f\"Flask response: {response_summary}\",\n                            \"status\": \"success\",\n                            \"response_time_ms\": response_time\n                        }\n                else:\n                    return {\n                        \"response\": f\"Flask returned status {response.status}\",\n                        \"status\": \"error\",\n                        \"response_time_ms\": response_time\n                    }\n                    \n        except Exception as e:\n            response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n            return {\n                \"response\": f\"Flask connection failed: {str(e)}\",\n                \"status\": \"failed\",\n                \"response_time_ms\": response_time,\n                \"error\": str(e)\n            }\n    \n    def _extract_flask_content(self, html_content: str) -> str:\n        \"\"\"Extract meaningful content from Flask HTML response\"\"\"\n        # Look for key indicators in Flask response\n        indicators = [\n            \"Pi Forge\", \"Quantum Genesis\", \"healthy\", \"dashboard\", \n            \"resonance\", \"visualization\", \"archetype\", \"collective wisdom\"\n        ]\n        \n        found_content = []\n        for indicator in indicators:\n            if indicator.lower() in html_content.lower():\n                found_content.append(indicator)\n        \n        if found_content:\n            return f\"Flask Glyph Weaver active - Found: {', '.join(found_content)}\"\n        else:\n            return f\"Flask response received ({len(html_content)} chars)\"\n    \n    async def _collect_gradio_response(self, query_data: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"Collect response from Gradio Truth Mirror\"\"\"\n        start_time = asyncio.get_event_loop().time()\n        \n        try:\n            # Gradio interface check\n            url = f\"{self.trinity_endpoints['gradio']}/\"\n            \n            async with self.session.get(url, timeout=15) as response:\n                response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n                \n                if response.status == 200:\n                    html_content = await response.text()\n                    gradio_indicators = self._extract_gradio_content(html_content)\n                    \n                    return {\n                        \"response\": f\"Gradio Truth Mirror active: {gradio_indicators}\",\n                        \"status\": \"success\",\n                        \"response_time_ms\": response_time\n                    }\n                else:\n                    return {\n                        \"response\": f\"Gradio returned status {response.status}\",\n                        \"status\": \"error\", \n                        \"response_time_ms\": response_time\n                    }\n                    \n        except Exception as e:\n            response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n            return {\n                \"response\": f\"Gradio connection failed: {str(e)}\",\n                \"status\": \"failed\",\n                \"response_time_ms\": response_time,\n                \"error\": str(e)\n            }\n    \n    def _extract_gradio_content(self, html_content: str) -> str:\n        \"\"\"Extract meaningful content from Gradio HTML response\"\"\"\n        gradio_indicators = [\n            \"gradio\", \"interface\", \"ethical\", \"audit\", \"veto\", \"triad\",\n            \"synthesis\", \"coherence\", \"canticle\", \"sovereign\"\n        ]\n        \n        found_indicators = []\n        for indicator in gradio_indicators:\n            if indicator.lower() in html_content.lower():\n                found_indicators.append(indicator)\n        \n        if found_indicators:\n            return f\"Ethical audit interface ready - Found: {', '.join(found_indicators[:5])}\"\n        else:\n            return f\"Gradio interface available ({len(html_content)} chars)\"\n    \n    async def _collect_integration_response(self, query_data: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"Collect cross-component integration response\"\"\"\n        start_time = asyncio.get_event_loop().time()\n        \n        try:\n            # Test integration by checking all components\n            integration_results = {\n                \"fastapi_status\": self.health_status.get(\"fastapi\", False),\n                \"flask_status\": self.health_status.get(\"flask\", False), \n                \"gradio_status\": self.health_status.get(\"gradio\", False)\n            }\n            \n            all_healthy = all(integration_results.values())\n            healthy_count = sum(integration_results.values())\n            \n            response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n            \n            integration_summary = f\"Sacred Trinity Integration: {healthy_count}/3 components healthy\"\n            if all_healthy:\n                integration_summary += \" - Full Trinity synchronization achieved\"\n            elif healthy_count >= 2:\n                integration_summary += \" - Partial Trinity coordination maintained\"\n            else:\n                integration_summary += \" - Trinity requires restoration\"\n            \n            return {\n                \"response\": integration_summary,\n                \"status\": \"success\" if healthy_count >= 2 else \"degraded\",\n                \"response_time_ms\": response_time,\n                \"integration_details\": integration_results\n            }\n            \n        except Exception as e:\n            response_time = (asyncio.get_event_loop().time() - start_time) * 1000\n            return {\n                \"response\": f\"Integration test failed: {str(e)}\",\n                \"status\": \"failed\",\n                \"response_time_ms\": response_time,\n                \"error\": str(e)\n            }\n    \n    def _create_error_response(self, query_data: Dict[str, Any], error: str) -> Dict[str, Any]:\n        \"\"\"Create error response to maintain dataset consistency\"\"\"\n        return {\n            **query_data,\n            \"response\": f\"Error during response collection: {error}\",\n            \"response_metadata\": {\n                \"collection_timestamp\": datetime.utcnow().isoformat(),\n                \"component_status\": False,\n                \"response_status\": \"error\",\n                \"response_time_ms\": 0,\n                \"error\": error\n            }\n        }\n    \n    async def save_responses_dataset(self, filename: str = \"trinity_responses.jsonl\") -> str:\n        \"\"\"Save collected responses as JSONL dataset\"\"\"\n        filepath = Path(filename)\n        \n        with open(filepath, 'w') as f:\n            for response_data in self.collected_responses:\n                f.write(json.dumps(response_data) + \"\\n\")\n        \n        logger.info(f\"💾 Saved {len(self.collected_responses)} responses to {filepath}\")\n        return str(filepath)\n    \n    def get_collection_summary(self) -> Dict[str, Any]:\n        \"\"\"Get summary of response collection\"\"\"\n        if not self.collected_responses:\n            return {\"status\": \"no_data\", \"message\": \"No responses collected\"}\n        \n        # Calculate statistics\n        total_responses = len(self.collected_responses)\n        successful_responses = sum(1 for r in self.collected_responses \n                                 if r.get(\"response_metadata\", {}).get(\"response_status\") == \"success\")\n        \n        # Component breakdown\n        component_stats = {}\n        for response in self.collected_responses:\n            component = response.get(\"component\", \"unknown\")\n            if component not in component_stats:\n                component_stats[component] = {\"total\": 0, \"successful\": 0}\n            component_stats[component][\"total\"] += 1\n            if response.get(\"response_metadata\", {}).get(\"response_status\") == \"success\":\n                component_stats[component][\"successful\"] += 1\n        \n        return {\n            \"status\": \"complete\",\n            \"total_responses\": total_responses,\n            \"successful_responses\": successful_responses,\n            \"success_rate\": successful_responses / total_responses if total_responses > 0 else 0,\n            \"component_breakdown\": component_stats,\n            \"trinity_health\": self.health_status,\n            \"collection_timestamp\": datetime.utcnow().isoformat()\n        }\n\nasync def main():\n    \"\"\"Main agent runner execution for testing\"\"\"\n    print(\"🤖 Sacred Trinity Agent Runner - Response Collection System\")\n    print(\"🌌 Testing Sacred Trinity architecture response collection...\")\n    \n    # Example test queries for demonstration\n    sample_queries = [\n        {\n            \"query\": \"Test FastAPI quantum conduit health and authentication\",\n            \"component\": \"fastapi\",\n            \"evaluation_focus\": \"authentication_security\",\n            \"test_id\": \"demo_fastapi_001\"\n        },\n        {\n            \"query\": \"Test Flask glyph weaver dashboard visualization\",\n            \"component\": \"flask\",\n            \"evaluation_focus\": \"visualization_accuracy\", \n            \"test_id\": \"demo_flask_001\"\n        },\n        {\n            \"query\": \"Test Gradio truth mirror ethical audit interface\",\n            \"component\": \"gradio\",\n            \"evaluation_focus\": \"ethical_processing\",\n            \"test_id\": \"demo_gradio_001\" \n        }\n    ]\n    \n    async with SacredTrinityAgentRunner() as agent_runner:\n        # Collect responses\n        responses = await agent_runner.run_comprehensive_collection(sample_queries)\n        \n        # Save dataset\n        dataset_file = await agent_runner.save_responses_dataset(\"demo_responses.jsonl\")\n        \n        # Print summary\n        summary = agent_runner.get_collection_summary()\n        print(\"\\n📊 Collection Summary:\")\n        print(json.dumps(summary, indent=2))\n        \n        print(f\"\\n💾 Responses saved to: {dataset_file}\")\n        print(\"✅ Sacred Trinity response collection complete!\")\n        \n        return responses\n\nif __name__ == \"__main__\":\n    asyncio.run(main())\n