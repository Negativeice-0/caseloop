git pull connection reset

# Git Pull Fails With "Recv failure: Connection was reset"

## Symptom

Attempting to pull from the safety branch:

```powershell
git pull --tags origin safety/main-20261119-142303
```

Results in:

```text
fatal: unable to access 'https://github.com/Negativeice-0/caseloop.git/':
Recv failure: Connection was reset
```

---

## Repository State

### Remote Configuration

```powershell
git remote -v
```

Output:

```text
origin  https://github.com/Negativeice-0/caseloop.git (fetch)
origin  https://github.com/Negativeice-0/caseloop.git (push)
```

Status: ✅ Correct

---

### Branch Configuration

```powershell
git branch -a
```

Output:

```text
main
* safety/main-20261119-142303

remotes/origin/HEAD -> origin/main
remotes/origin/main
remotes/origin/safety/main-20261119-142303
```

Status: ✅ Correct

Observations:

- Local safety branch exists.
- Remote safety branch exists.
- Origin is configured correctly.
- Branch names match.

This strongly suggests the issue is not caused by an invalid branch name or missing remote branch.

---

## Most Likely Cause

Network interruption between the local machine and GitHub.

The message:

```text
Recv failure: Connection was reset
```

typically means:

- GitHub accepted the connection.
- Data transfer started.
- The connection was terminated unexpectedly.

Possible sources:

- VPN interruption
- Antivirus HTTPS inspection
- Firewall interference
- Proxy configuration issues
- ISP instability
- Temporary GitHub connectivity issue
- Corporate network restrictions

---

## Diagnostic Steps

### 1. Verify GitHub Reachability

```powershell
curl -I https://github.com
```

Expected:

```text
HTTP/1.1 200 OK
```

If this fails:

- Check internet connection.
- Verify firewall settings.
- Disable VPN and retest.

---

### 2. Verify Repository Access

```powershell
git ls-remote origin
```

Expected:

```text
<hash> HEAD
<hash> refs/heads/main
<hash> refs/heads/safety/main-20261119-142303
...
```

Results:

| Result | Meaning |
|----------|----------|
| Succeeds | Network path to GitHub is good |
| Same reset error | Network problem is confirmed |
| Authentication error | Credential issue |
| Repository not found | Wrong URL or permissions |

---

### 3. Enable Verbose Git Networking

```powershell
$env:GIT_TRACE=1
$env:GIT_CURL_VERBOSE=1

git pull --tags origin safety/main-20261119-142303
```

Review where the transfer stops.

---

## Common Fixes

### Fix 1: Retry

```powershell
git pull --tags origin safety/main-20261119-142303
```

Many connection reset issues are transient.

---

### Fix 2: Force HTTP/1.1

Some environments have issues with HTTP/2.

```powershell
git config --global http.version HTTP/1.1
```

Retry:

```powershell
git pull --tags origin safety/main-20261119-142303
```

To verify:

```powershell
git config --global --get http.version
```

Expected:

```text
HTTP/1.1
```

---

### Fix 3: Fetch First

Instead of pull:

```powershell
git fetch origin
```

Then:

```powershell
git status
```

If fetch succeeds:

```powershell
git merge origin/safety/main-20261119-142303
```

---

### Fix 4: Disable VPN

If a VPN is active:

1. Disconnect VPN.
2. Close PowerShell.
3. Reopen terminal.
4. Retry the pull.

---

### Fix 5: Temporarily Disable SSL Inspection

Some antivirus products interfere with Git HTTPS traffic.

Common products:

- Kaspersky
- Avast
- BitDefender
- ESET
- Sophos

Temporarily disable HTTPS scanning and retest.

---

## Additional Verification

Check remote references:

```powershell
git ls-remote --heads origin
```

Check origin information:

```powershell
git remote show origin
```

Check Git version:

```powershell
git --version
```

Older Git versions occasionally exhibit network issues.

---

## Recovery Option

If the branch already exists locally and only needs to be examined:

```powershell
git checkout safety/main-20261119-142303
git log --oneline -20
```

Since both local and remote safety branches are visible, immediate recovery work may still be possible even while network troubleshooting continues.

---

## Current Assessment

Based on the available evidence:

✅ Remote URL is valid.

✅ Local safety branch exists.

✅ Remote safety branch exists.

✅ Branch naming is correct.

❌ Git transfer is being interrupted during network communication.

**Root cause is most likely network transport related rather than repository configuration related.**