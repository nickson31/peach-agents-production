--- name: messaging-skill
description: Comprehensive messaging handling for various platforms including message composition, delivery confirmation, reading, and archiving. Use when the agent needs to: (1) Send messages to users/channels, (2) Read and respond to incoming messages, (3) Manage message history and archives, (4) Handle cross-platform messaging operations.
---
# Messaging Skill

## Overview
This skill provides comprehensive messaging capabilities across various platforms, enabling the agent to send, receive, manage, and archive messages efficiently.

## Core Functionality

### Message Operations
- **Send Messages**: Deliver messages to specified users or channels
- **Read Messages**: Access and process incoming communications
- **Reply Management**: Handle message responses and acknowledgments
- **Archive Operations**: Store and retrieve message history

### Platform Support
- Multi-platform messaging integration
- Cross-platform message routing
- Platform-specific formatting and handling

## Usage Guidelines

### When to Use This Skill
Use this skill whenever the agent needs to:
- Send a message to a user or channel
- Read and respond to incoming messages
- Search or retrieve message history
- Manage message archives and backups
- Handle messaging-related workflows

### Basic Operations

#### Sending Messages
```bash
# Example message sending workflow
message-send --target "user123" --content "Hello there!" --channel "telegram"
```

#### Reading Messages
```bash
# Retrieve recent messages
message-read --limit 10 --channel "telegram"
```

#### Message Management
```bash
# Archive important messages
message-archive --message-id "msg456" --category "important"
```

## Configuration
Configure platform-specific settings in the references/configuration.md file for optimal performance.

## Security Considerations
- Always verify message recipients
- Handle sensitive communications securely
- Follow platform-specific privacy policies
- Implement proper access controls for message archives

## Best Practices
- Always include clear context in messages
- Use appropriate channels for different message types
- Maintain organized message archives
- Respect user preferences for communication frequency
- Handle errors gracefully and provide appropriate feedback

## Troubleshooting
Common issues and solutions are documented in references/troubleshooting.md.