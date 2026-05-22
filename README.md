# Agentic AI Orchestrator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An intelligent Tool-Augmented Retrieval system that dynamically routes queries between a static historical corpus and real-time web search. 

This project demonstrates advanced Agentic AI orchestration using the Model Context Protocol (MCP) pattern. The agent evaluates user intent and synthesizes answers by invoking specialized tools, providing a hybrid approach to Information Retrieval (IR).

## 🏗️ Architecture

The orchestrator leverages a Large Language Model as its core reasoning engine, integrated with two distinct retrieval tools:
1. **The Static Archive (OpenWebText):** A local vector database containing a subset of the OpenWebText corpus, used for retrieving historical data.
2. **Live Google Search (Serper API):** A real-time web search integration, invoked dynamically when the agent detects a need for current events, breaking news, or facts outside its static training distribution.