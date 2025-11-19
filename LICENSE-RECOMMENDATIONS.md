# Licensing Analysis & Recommendations

**Date**: 2025-11-19
**Project**: Super Agent Monitor

---

## Reference Projects Licensing

### 1. multi-agent-workflow (apolopena/multi-agent-workflow)

**Status**: Needs verification when cloning
**Expected**: MIT License (common for open-source monitoring tools)
**Action Required**:
```bash
# After cloning, check license
cat external/multi-agent-workflow/LICENSE
```

### 2. claude-code-proxy

**Status**: Needs verification
**Expected**: MIT or Apache 2.0
**Action Required**:
```bash
# After installing, check license
npm info claude-code-proxy license
```

---

## Recommended License: **MIT License**

### Why MIT?

1. **Compatible with Dependencies**: If multi-agent-workflow and claude-code-proxy are MIT, we maintain compatibility
2. **Maximum Flexibility**: Allows commercial use, modification, distribution
3. **Simple & Clear**: Easy for users to understand their rights
4. **Industry Standard**: 80%+ of JavaScript/TypeScript projects use MIT

### IP Protection Considerations

**With MIT License:**
- ✅ You retain copyright
- ✅ Users can use/modify freely
- ❌ Cannot prevent competitive forks
- ❌ No patent protection

**Upgrade Options (if needed later):**
- **Dual licensing**: MIT for open source + Commercial license for closed-source use
- **Business Source License (BSL)**: Free for non-commercial, paid for commercial (Cockroach Labs model)
- **AGPL**: Requires SaaS users to open source their code (strong copyleft)

### **Recommendation: Start with MIT, evaluate after traction**

**Reasoning:**
1. **MVP Phase**: Focus on adoption, not IP protection
2. **Community Building**: MIT encourages contributions
3. **Pivot Later**: Can always add commercial licensing for enterprise features
4. **Examples**:
   - Sentry: MIT core + paid hosted service
   - GitLab: MIT core + paid enterprise features
   - Ghost: MIT + paid managed hosting

---

## Attribution Requirements

### If multi-agent-workflow is MIT:

**Required Attribution:**
```markdown
# ATTRIBUTIONS.md

## multi-agent-workflow

Copyright (c) [year] [author name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full MIT license text]
```

**In README.md:**
```markdown
## Acknowledgments

This project uses [multi-agent-workflow](https://github.com/apolopena/multi-agent-workflow)
by @apolopena for monitoring capabilities, licensed under MIT.
```

**In Code Comments:**
```typescript
// File: backend/src/api/monitoring.ts
// Portions adapted from multi-agent-workflow by @apolopena
// Licensed under MIT License
```

---

## Proposed LICENSE File

**File**: `LICENSE`

```
MIT License

Copyright (c) 2025 [Your Name or Company]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## IP Protection Strategy (Future)

### Phase 1 (Now - MVP): MIT License
- Open source everything
- Build community + trust
- Validate product-market fit

### Phase 2 (Month 6 - Traction): Dual Licensing
- Core features: MIT (open source)
- Enterprise features: Commercial license
  - SSO/SAML integration
  - Multi-tenancy
  - Priority support
  - SLA guarantees

### Phase 3 (Month 12 - Scale): SaaS Model
- Self-hosted: Free (MIT)
- Cloud hosted: Paid ($49-$499/month tiers)
- Examples: Sentry, PostHog, Plausible

---

## Checklist Before First Commit

- [ ] Verify multi-agent-workflow license (check `external/multi-agent-workflow/LICENSE`)
- [ ] Verify claude-code-proxy license (`npm info claude-code-proxy license`)
- [ ] Create `LICENSE` file with MIT License
- [ ] Create `ATTRIBUTIONS.md` listing all dependencies
- [ ] Add "License: MIT" badge to README.md
- [ ] Add acknowledgments section to README.md
- [ ] If using non-MIT dependencies, document compatibility

---

## License Compatibility Matrix

| Our License | Dependency License | Compatible? | Notes |
|-------------|-------------------|-------------|-------|
| MIT | MIT | ✅ Yes | Perfect match |
| MIT | Apache 2.0 | ✅ Yes | Can use, must include NOTICE |
| MIT | BSD | ✅ Yes | Similar to MIT |
| MIT | GPL | ❌ No | GPL requires our code to be GPL |
| MIT | AGPL | ❌ No | AGPL is even stricter |
| MIT | Proprietary | ⚠️ Maybe | Check terms |

---

## Action Items (Before Git Push)

1. **Clone Reference Repos:**
   ```bash
   cd external
   git clone https://github.com/apolopena/multi-agent-workflow.git
   # Check license: cat multi-agent-workflow/LICENSE
   ```

2. **Verify License:**
   ```bash
   # If MIT: ✅ Proceed with MIT for our project
   # If GPL: ❌ STOP - need to reconsider architecture
   # If Apache 2.0: ✅ OK, but add NOTICE file
   ```

3. **Create LICENSE:**
   ```bash
   # Use template above, replace [Your Name or Company]
   cp LICENSE-TEMPLATE LICENSE
   ```

4. **Create ATTRIBUTIONS.md:**
   ```bash
   # List all dependencies with licenses
   echo "# Third-Party Licenses" > ATTRIBUTIONS.md
   # Copy multi-agent-workflow/LICENSE content
   ```

5. **Update README.md:**
   ```markdown
   ## License
   MIT License - see [LICENSE](LICENSE)

   ## Acknowledgments
   - [multi-agent-workflow](https://github.com/apolopena/multi-agent-workflow) by @apolopena
   ```

6. **Add License Badge:**
   ```markdown
   ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
   ```

---

## Recommended LICENSE File (Ready to Use)

**Create this file as `/home/user/super_agent_monitor/LICENSE`:**

```
MIT License

Copyright (c) 2025 Super Agent Monitor Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Summary

**Recommendation**: Use MIT License with clear attribution to dependencies.

**Benefits:**
- ✅ Maximum flexibility for users
- ✅ Compatible with most open-source licenses
- ✅ Builds community trust
- ✅ Can upgrade to dual licensing later
- ✅ Simple and well-understood

**Next Steps:**
1. Verify multi-agent-workflow is MIT (when cloning)
2. Create LICENSE file
3. Create ATTRIBUTIONS.md
4. Update README with license info
5. Commit and push

**If Commercial Protection Needed:**
- Wait until traction (50+ users)
- Add enterprise features under separate license
- Keep core MIT for community
