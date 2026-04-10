# Security Policy

## Security Overview

This document outlines the security considerations for the Python Features Explorer application.

## Current Security Model

The application has a **permissive security model** by default to provide maximum flexibility for learning purposes.

### What This Means

- **Examples run with user privileges** - Example scripts execute with full access to your system
- **No sandboxing by default** - Code execution does not use isolation containers
- **File system access** - Scripts can read/write files in accessible directories
- **Network access** - Scripts can make network connections (unless restricted by system firewall)

## Known Security Considerations

### 1. Arbitrary Code Execution

**Risk Level:** ⚠️ Medium

**Description:** The application executes any Python script in the `examples/` directory without validation.

**Impact:** Malicious scripts could potentially:
- Read or modify files on your system
- Access system resources
- Make network connections
- Install unauthorized software

**Mitigation:**
- Only run examples from trusted sources
- Review example code before execution
- Use separate user accounts for testing
- Consider running in a containerized environment

### 2. Path Validation

**Risk Level:** ✓ Accepted

**Description:** The application validates that examples are `.py` files, but does not restrict file system locations.

**Security Note:** Path construction is designed to only access the designated `examples/` directory.

### 3. Code Execution Timeout

**Risk Level:** ✓ Mitigated

**Description:** All examples are subject to timeout protection.

**Settings:**
- Default timeout: 30 seconds (configurable in `config.yaml`)
- Prevents infinite loops and resource exhaustion
- Automatically kills hanging processes

## Security Recommendations

### For Production Use

1. **Enable Sandbox Mode** (`sandbox_mode: true`)
   - Adds file system access restrictions
   - Limits allowed directories
   - Blocks potentially dangerous functions

2. **Review Allowed Directories**
   ```yaml
   security:
     allowed_directories: 
       - "examples"  # Only these can be accessed
   ```

3. **Monitor Blocked Functions**
   ```yaml
   security:
     blocked_functions: 
       - "os.system"      # Prevents shell commands
       - "os.popen"
       - "subprocess.call"
       - "eval"          # Prevents arbitrary code execution
       - "exec"          # Prevents arbitrary code execution
   ```

4. **Logging**
   - Keep detailed logs of all executions
   - Review logs periodically
   - Set log rotation for security monitoring

5. **Use Non-Privileged User**
   - Run application as separate user
   - Limit user file system permissions
   - Use read-only mounts where possible

### For Development/Testing

1. **Use Virtual Environment**
   ```bash
   python -m venv explorer_env
   source explorer_env/bin/activate
   ```

2. **Use Containerization**
   ```bash
   docker run -v $(pwd):/app explorer_image
   ```

3. **Enable Strict Logging**
   ```yaml
   logging:
     level: "DEBUG"
     file: "secure_logs/python_explorer.log"
     max_size_mb: 50
   ```

## Security Best Practices

### Before Running Examples

1. **Review the code** - Understand what the example does
2. **Check imports** - Ensure no suspicious external packages
3. **Monitor output** - Watch for unexpected behavior
4. **Start small** - Begin with simple examples

### After Installing/Running

- **Keep Python updated** - Update regularly for security patches
- **Review dependencies** - Check for vulnerable packages with `pip audit`
- **Check logs** - Regularly review `python_explorer.log`
- **Back up progress** - Periodically backup `user_progress.json`

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:

1. **Do not disclose publicly** until resolved
2. **Email security maintainers** with details
3. **Include:**
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)

## Security Updates

Security updates will be announced:
- Through repository releases
- Via email notifications for subscribed users
- On the project's security page

## Version Support

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | ✅ Active Security |
| 1.0.x   | ⚠️ Security Only  |

## Audit Trail

For comprehensive security auditing:
- All executions are logged to `python_explorer.log`
- User progress changes tracked with timestamps
- Failed executions recorded with error details
- Configuration changes logged

## External Security Tools

Consider using additional tools for comprehensive security:

1. **SAST (Static Application Security Testing)**
   - Code analysis before execution
   - Detects common vulnerabilities

2. **Containerization**
   ```bash
   # Run in isolated container
   docker run --read-only --tmpfs /tmp explorer_app
   ```

3. **Network Security**
   - Use firewall to restrict network access
   - Monitor outgoing connections
   - Consider using air-gapped systems

## Compliance Considerations

### Educational Use

For educational purposes, the default permissive model balances:
- Learning flexibility
- Resource accessibility
- System integration

### Production Use

For production/deployed versions:
- Enable sandbox mode by default
- Restrict examples to trusted sources
- Implement comprehensive logging
- Use containerized execution

## Known Limitations

1. **No OS-level sandboxing** - Requires external tools for containers (Docker, etc.)
2. **No file system virtualization** - Scripts have real file system access
3. **No network isolation** - Unless system firewall configured
4. **No capability dropping** - Scripts run with user privileges

## Third-Party Security

- Dependencies listed in `requirements.txt` are periodically audited
- Python itself receives regular security updates
- Consider using package scanning tools:
  - `safety` for vulnerability scanning
  - `pip-audit` for dependency checks
  - `bandit` for Python security analysis

## Future Security Improvements

Planned security enhancements:
- [ ] Container-based execution
- [ ] File system sandboxing
- [ ] Network isolation
- [ ] Permission-based execution controls
- [ ] Automated vulnerability scanning

## Contact

For security-related inquiries:
- Issue tracker: Security section
- Email: Use repository issue system
- Timeframe: Within 48 hours for valid reports

## Disclaimer

**This software is provided "as is" without warranty of any kind.**

The development team takes security seriously but cannot guarantee absolute security, especially with applications that execute user-provided code. Use at your own risk and implement appropriate security measures based on your specific requirements.

---

*Last updated: April 2024*
