# MCP SDK Implementation

This directory contains a Demo wit Web UI using the actual Model Context Protocol (MCP) SDK.

## Architecture Overview

This implementation uses the official MCP SDK to create proper MCP servers and clients.

### Original Implementation (in parent directories)
- **mcp_server_project**: Mock MCP server for agent registration and message relay
- **agent_a_project**: Frontend agent that initiates document verification/summarization requests
- **agent_b_project**: Backend agent that provides summarization services using Azure OpenAI

### New MCP SDK Implementation

#### Servers (`/servers/`)
- **document_verification_server**: MCP server that provides document verification tools
- **summarization_server**: MCP server that provides text summarization tools using Azure OpenAI

#### Clients (`/clients/`)
- **document_client**: MCP client that uses document verification services
- **summarization_client**: MCP client that uses summarization services

#### Shared (`/shared/`)
- **crypto_utils.py**: Shared cryptographic utilities for secure communication
- **config.py**: Shared configuration and environment variables

## Key Differences from Original

1. **Protocol**: Uses actual MCP protocol instead of custom REST API
2. **Communication**: MCP tools and resources instead of encrypted HTTP requests
3. **Architecture**: Proper MCP server/client model instead of peer-to-peer agents
4. **Security**: MCP-native security features alongside custom encryption
5. **Discoverability**: MCP schema for automatic tool discovery

## Setup Instructions

** Follow the Quickstart Instructions to get started!

1. Install MCP SDK: `pip install mcp`
2. Configure Azure OpenAI credentials in environment variables
3. Run servers: Each server can be started independently
4. Connect clients: Clients can discover and use server capabilities

## Security Model

- Maintains encryption for sensitive data transmission
- Leverages MCP's built-in transport security
- Access control through MCP server authentication
- Public key exchange for document verification

## Migration Benefits

- Standard protocol compliance
- Better tool discovery and schema validation
- Improved error handling and logging
- Enhanced scalability and interoperability
- Ecosystem compatibility with MCP-aware applications


