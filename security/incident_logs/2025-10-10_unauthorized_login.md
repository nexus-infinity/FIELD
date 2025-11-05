# Security Incident Report: Unauthorized cPanel Login
**Date**: 2025-10-10
**Time**: 08:45:41 AM UTC
**Incident Type**: Unauthorized Login from Unknown Network

## Login Details
- **Domain**: berjak.com.au
- **Service**: cpaneld
- **Username**: walkerv4
- **Authentication Database**: system

## Network Information
### Remote Connection
- **Remote IP**: 10.25.32.158 (Class A private network)
- **Remote Port**: 48128 (non-standard, possibly randomized)
- **Known Network**: No
- **Connection Type**: Likely VPN/proxy masked
- **Intrusion Sophistication**: High - using network obfuscation

### Local Server
- **Local IP**: 185.184.155.45
- **Local Port**: 2083

## Initial Observations
1. Login was successful, indicating valid credentials were used
2. Connection originated from an unrecognized network
3. Access was through cPanel's web interface
4. System generated an automatic notification due to unknown network access
5. Server identified as cp-wc35.per01.ds.network (Crazy Domains/ds.network)
6. Account has both SSH key access and cPanel web interface access

## Immediate Concerns
1. How the credentials were obtained
2. Whether other accounts may be compromised
3. What actions were taken during the unauthorized session
4. Potential data exfiltration risk
5. Status and security of SSH key (~/.ssh/berjak_walkerv4)
6. Whether cPanel and SSH passwords were changed separately from keys

## Recommendations
1. Immediate password reset for all cPanel accounts
2. Enable two-factor authentication if not already active
3. Review all file changes and access logs during the time of compromise
4. Implement IP-based access restrictions
5. Audit all user accounts and access permissions
6. Replace SSH key pair for walkerv4 account
7. Verify SSH key permissions and containment
8. Review and potentially restrict cPanel API access

## Follow-up Actions Required
- [ ] Complete security audit of server
- [ ] Review all recent file modifications
- [ ] Check for unauthorized configuration changes
- [ ] Verify integrity of web applications
- [ ] Monitor for additional suspicious activity

## Notes
- This incident appears to be a targeted login rather than an automated attack
- The use of a private IP address (10.25.32.158) suggests possible VPN or proxy usage
- Successful authentication indicates credential compromise rather than exploitation