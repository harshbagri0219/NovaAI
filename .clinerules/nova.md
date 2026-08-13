# Project NOVA — Development Rules & Knowledge

## 1. Project Identity

Project name: NOVA.

NOVA is a modular, offline-first personal AI assistant designed
to operate primarily on Android and other user-controlled systems.

NOVA should progressively develop capabilities in:

- Artificial intelligence
- Machine learning
- Natural language processing
- Voice interaction
- Computer vision
- Programming
- System administration
- Cybersecurity
- Defensive security
- Authorized penetration testing
- Digital forensics
- Network analysis
- Automation
- Android system interaction
- Knowledge management
- Personal memory
- Reasoning
- Planning
- Task execution

NOVA is a long-term project and should be designed for continuous
extension rather than as a single monolithic application.


# 2. Core Vision

NOVA should eventually provide:

- Natural voice interaction
- Persistent personal memory
- Context-aware conversation
- Reasoning
- Planning
- Task execution
- Local AI models
- Android device interaction
- Android automation
- Coding assistance
- Document processing
- Image understanding
- Computer vision
- Knowledge retrieval
- Continuously updateable knowledge
- System monitoring
- Defensive cybersecurity
- Authorized security testing
- Proactive assistance


# 3. Development Philosophy

NOVA must be:

- Modular
- Maintainable
- Testable
- Privacy-focused
- Offline-first where practical
- Secure by default
- Explainable
- Recoverable
- Extensible
- Permission-based for impactful actions

Do not create unnecessary complexity.

Prefer small independent modules over huge files.

Prefer reusable components over duplicated code.


# 4. User Control

The user remains the final authority.

NOVA must not silently perform consequential actions.

Actions involving:

- deleting data
- modifying important system settings
- sending communications
- installing software
- changing security configuration
- executing potentially dangerous commands
- performing security testing
- modifying network configuration

should use appropriate confirmation and permission mechanisms.

NOVA should clearly explain:

1. What it wants to do.
2. Why it wants to do it.
3. What effect it may have.
4. Whether confirmation is required.


# 5. AI Architecture

The intended architecture is:

User
↓
Voice/Text Interface
↓
Intent Detection
↓
Context
↓
Memory
↓
Knowledge Retrieval
↓
Reasoning
↓
Planning
↓
Permission/Safety Layer
↓
Task Coordination
↓
Tool/Plugin Selection
↓
Execution
↓
Result Analysis
↓
Response Generation


# 6. Memory System

NOVA should maintain structured long-term memory.

Memory categories may include:

- User preferences
- Languages
- Hobbies
- Goals
- Projects
- Frequently used commands
- Important configuration
- Conversation context
- Learned facts
- Task history

Memory should be normalized.

For example:

python
Python
PYTHON
python.

should represent the same language.

NOVA should avoid storing duplicate facts.

Sensitive information should not automatically be stored.


# 7. Context System

NOVA should understand:

- Current conversation
- Previous messages
- References such as "it", "that", "this", "the previous one"
- Recently mentioned entities
- User preferences
- Current task
- Previous task results

Example:

User:
I like Python and Java.

User:
Which one is better for AI?

NOVA should understand that "which one" refers to Python and Java.


# 8. Reasoning

NOVA should distinguish between:

- Facts
- User preferences
- Opinions
- Inferences
- Uncertainty

NOVA should not present guesses as facts.

When information is uncertain, NOVA should communicate uncertainty.

Reasoning should be separated from tool execution.


# 9. Planning

NOVA should eventually support:

- Single-step tasks
- Multi-step tasks
- Conditional tasks
- Scheduled tasks
- Long-running tasks
- Task dependencies
- Error recovery

Plans should be inspectable before consequential execution.


# 10. Tool and Plugin Architecture

Capabilities should preferably be implemented as plugins/tools.

Examples:

- Battery
- Storage
- Device information
- Time
- System status
- Memory
- Network information
- File operations
- Android automation
- AI inference
- Document processing
- Security analysis

Plugins should have:

- Clear inputs
- Clear outputs
- Error handling
- Permission requirements
- Logging where appropriate
- Tests


# 11. Cybersecurity Knowledge

NOVA should develop strong cybersecurity knowledge.

Cybersecurity domains include:

## Networking

- TCP/IP
- UDP
- DNS
- HTTP/HTTPS
- TLS
- SSH
- Routing
- NAT
- Firewalls
- VPNs
- Proxies
- Network segmentation
- Wireless networking

## Operating Systems

- Linux
- Android
- Windows
- Filesystems
- Processes
- Permissions
- Services
- System calls
- Authentication
- Access control

## Security Fundamentals

- CIA triad
- Authentication
- Authorization
- Accounting
- Cryptography
- Hashing
- Digital signatures
- Certificates
- Key management
- Secure software development
- Threat modeling
- Risk assessment

## Web Security

NOVA should understand defensive and authorized testing concepts
including:

- Authentication vulnerabilities
- Authorization failures
- Session security
- Input validation
- Injection vulnerabilities
- XSS
- CSRF
- SSRF
- File upload security
- Path traversal
- API security
- Security headers
- Secure cookies
- Rate limiting

## System Security

- Hardening
- Patch management
- Vulnerability management
- Logging
- Monitoring
- Endpoint protection
- Least privilege
- Secure configuration
- Incident response

## Digital Forensics

NOVA should understand:

- Evidence preservation
- File metadata
- Log analysis
- Timeline analysis
- Hash verification
- Disk analysis
- Memory analysis
- Network evidence
- Chain of custody

## Security Monitoring

NOVA should be capable of monitoring for:

- Suspicious processes
- Unexpected network connections
- Configuration changes
- Authentication anomalies
- Newly disclosed vulnerabilities
- Security advisories
- Malware indicators

NOVA may recommend defensive actions and, where explicitly
pre-approved, automate safe defensive measures.


# 12. Red Team / Penetration Testing

NOVA may support authorized security research and penetration testing.

Its knowledge may include:

- Reconnaissance concepts
- Asset discovery
- Port/service identification
- Enumeration
- Vulnerability assessment
- Threat modeling
- Exploitation concepts
- Privilege escalation concepts
- Post-exploitation concepts
- Detection engineering
- Security validation
- Reporting
- Remediation

All penetration testing should be performed only against:

- Systems owned by the user
- Systems where the user has explicit authorization
- Intentionally vulnerable laboratory environments
- CTF platforms
- Educational environments

NOVA should encourage defining the authorized scope before testing.

NOVA should maintain clear boundaries between:

- Reconnaissance
- Assessment
- Exploitation
- Post-exploitation
- Cleanup
- Reporting


# 13. Black Hat Knowledge — Educational Understanding

NOVA may maintain knowledge about how malicious attackers operate
for the purpose of:

- Threat modeling
- Detection
- Defense
- Security education
- Incident response
- Authorized red-team simulations

Relevant knowledge areas include:

- Malware behavior
- Phishing techniques
- Credential theft concepts
- Persistence mechanisms
- Command-and-control concepts
- Evasion concepts
- Privilege escalation concepts
- Lateral movement
- Data exfiltration concepts
- Botnets
- Ransomware behavior
- Supply-chain attacks
- Social engineering
- Exploit development concepts

This knowledge should primarily be used to understand, detect,
simulate safely, and defend against threats.

NOVA must not interpret "black hat knowledge" as permission to
attack arbitrary real-world systems.

Do not remove safety boundaries merely because a task is described
as hacking.


# 14. Kali Linux Integration

NOVA should eventually be capable of integrating with a Kali Linux
laboratory environment for authorized security testing.

Potential integrations include:

- Nmap
- Wireshark
- Burp Suite
- Metasploit
- Nikto
- Gobuster
- John the Ripper
- Hashcat
- Aircrack-ng
- Linux networking utilities
- Security scanners

Tools should be exposed through controlled plugins rather than
allowing unrestricted command execution.

Each security tool should define:

- Purpose
- Required permissions
- Input
- Output
- Authorized scope
- Risk level
- Logging behavior


# 15. Defensive Security

NOVA should prioritize defensive cybersecurity.

Long-term capabilities may include:

- Vulnerability monitoring
- Security advisory monitoring
- Patch recommendations
- System hardening
- Network monitoring
- Suspicious activity detection
- Security alerts
- Configuration auditing
- Dependency vulnerability checking
- Secret detection
- Malware indicators
- Incident response assistance

NOVA should explain:

- What threat was detected
- Why it matters
- What systems may be affected
- Recommended action
- What action NOVA performed
- What action still requires user approval


# 16. Adaptive Security

NOVA should eventually monitor newly disclosed cybersecurity
threats and vulnerabilities.

Potential sources include:

- CVE information
- Vendor security advisories
- CERT advisories
- Security research
- Package vulnerability databases

NOVA should be capable of:

1. Detecting relevant vulnerabilities.
2. Determining whether the user's system may be affected.
3. Explaining the risk.
4. Recommending remediation.
5. Applying pre-approved defensive actions where safe.
6. Reporting exactly what changed.

Automatic security changes must have clear permission controls.


# 17. Android Security

NOVA should eventually understand Android security concepts including:

- Android permissions
- Applications
- Services
- Activities
- Broadcast receivers
- Content providers
- ADB
- Termux
- Package management
- Network configuration
- Storage permissions
- Device security
- Application isolation
- SELinux concepts
- Root/non-root environments

Root access should never be assumed.

NOVA should detect its current privilege level before attempting
privileged operations.


# 18. Offline-First Design

Core functionality should work without internet access where practical.

Possible local components:

- Local LLM
- Local speech recognition
- Local text-to-speech
- Local embeddings
- Local vector database
- Local knowledge base
- Local memory
- Local task engine

Online services should be optional.


# 19. Knowledge System

NOVA should eventually maintain a continuously updateable
knowledge system.

Knowledge should be separated into:

- Static knowledge
- User knowledge
- Current information
- Project knowledge
- Security intelligence
- Temporary context

Knowledge sources should be tracked where possible.

NOVA should distinguish:

"Known"
from
"Recently retrieved"
from
"Inferred"


# 20. Coding Intelligence

NOVA should eventually understand and assist with:

- Python
- Java
- JavaScript/TypeScript
- C
- C++
- Rust
- Go
- Kotlin
- Bash
- SQL
- HTML
- CSS
- PowerShell
- Assembly concepts

Python is currently the primary language for the NOVA prototype.

Java is also an important language of interest for the user.


# 21. Development Environment

Primary development:

- Windows laptop
- VS Code
- Cline
- Git
- GitHub

Secondary development/testing:

- Android
- Termux

Android should primarily be used for:

- Runtime testing
- Android integration
- Device interaction
- Automation testing
- Performance testing


# 22. Git Workflow

Before major changes:

1. Check git status.
2. Create a checkpoint if necessary.
3. Make a small change.
4. Compile.
5. Run tests.
6. Run the application.
7. Verify behavior.
8. Review git diff.
9. Commit.
10. Push.

Never destroy working code without a recoverable checkpoint.


# 23. Testing

Python compilation should be checked with:

python -m py_compile ...

The full test suite should eventually be run with:

pytest

Important functionality should have automated tests.


# 24. Secrets

Never store:

- GitHub tokens
- API keys
- Passwords
- Private keys
- Authentication credentials
- Personal secrets

in source code or documentation.

Use environment variables or secure secret storage.


# 25. Cline Behavior

Before modifying code:

1. Read this file.
2. Inspect the repository.
3. Read relevant documentation.
4. Identify dependencies.
5. Explain the planned change.
6. Make the smallest reasonable modification.
7. Test the modification.
8. Report the result.

Do not rewrite the entire project unless explicitly requested.

Do not create duplicate modules.

Do not assume functionality exists without checking.

Preserve working functionality.

When uncertain about a major architectural decision,
ask the user before proceeding.


# 26. Current Project State

Current NOVA prototype version:

v0.1.0

The current prototype already contains:

- Memory
- Profile knowledge
- Learning
- Intent detection
- Context
- Context building
- Context resolution
- Reasoning
- Decision engine
- Planning
- Task planning
- Task coordination
- Task execution
- Result analysis
- Plugins
- Routing
- Voice
- System monitoring
- Battery monitoring
- Storage monitoring
- Device information
- Tests

The project should continue from the existing implementation.

Do NOT rebuild NOVA from scratch.


# 27. Immediate Development Direction

The next major milestone is:

NOVA v0.2

Primary focus:

Structured and normalized long-term memory.

The next area to inspect is:

ai/learning.py

Integration should involve:

knowledge/profile.py
memory/
brain/context.py
brain/context_builder.py

The objective is to make NOVA capable of storing and retrieving
structured preferences reliably.

Example:

User:
I like Python and Java.

NOVA should store:

languages:
    Python
    Java

Then:

User:
Which one is better for AI?

NOVA should retrieve the relevant languages and reason about them.

Do not hard-code this specific conversation.

The system should generalize to other preferences and entities.