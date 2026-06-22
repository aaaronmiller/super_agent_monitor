# Licensing Analysis & Recommendations

**Date**: 2025-11-19 (Updated)
**Project**: Super Agent Monitor

---

## Reference Projects Licensing

### 1. multi-agent-workflow (apolopena/multi-agent-workflow)

**Status**: ⚠️ **UNLICENSED** (as of 2025-11-19)
**Legal Status**: All rights reserved by original authors
**Risk**: Using unlicensed code without permission is legally uncertain
**Mitigation**: Reference only, prepared to rewrite if necessary

### 2. claude-code-proxy

**Status**: ⚠️ **UNLICENSED** (as of 2025-11-19)
**Legal Status**: All rights reserved by original authors
**Risk**: Using unlicensed code without permission is legally uncertain
**Mitigation**: Reference only, prepared to rewrite if necessary

**IMPORTANT**: See NOTICE file for full details on unlicensed dependencies.

---

## Chosen License: **Elastic License 2.0**

### Why Elastic License 2.0?

1. **Source-Available**: Code is visible on GitHub for transparency
2. **Commercial Protection**: Prevents others from offering as a competing service
3. **Allows Modification**: Users can fork, modify, and use internally
4. **Commercialization Path**: You can sell licenses or offer SaaS exclusively
5. **Industry Precedent**: Used by Elasticsearch, Kibana, and other successful projects

### License Characteristics

**What Users CAN Do:**
- ✅ View, copy, and modify the source code
- ✅ Use internally within their organization
- ✅ Create derivative works
- ✅ Distribute modified versions (with same license)

**What Users CANNOT Do:**
- ❌ Offer the software as a managed/hosted service to third parties
- ❌ Remove or obscure licensing notices
- ❌ Circumvent license key functionality (if added)

### IP Protection Advantages

**With Elastic License 2.0:**
- ✅ You retain copyright
- ✅ Prevents SaaS competition (AWS can't offer "Super Agent Monitor as a Service")
- ✅ GitHub-friendly (still visible as open source)
- ✅ Can sell commercial licenses
- ✅ Can offer official SaaS exclusively
- ✅ Patent protection included

### Comparison with Alternatives

| License | SaaS Protection | Fork-Friendly | Commercial Use | GitHub Stars Potential |
|---------|----------------|---------------|----------------|----------------------|
| MIT | ❌ No | ✅ Yes | ✅ Yes | ⭐⭐⭐⭐⭐ |
| AGPL | ⚠️ Partial | ❌ No | ⚠️ Restricted | ⭐⭐⭐ |
| **Elastic 2.0** | ✅ Yes | ✅ Yes | ✅ Yes | ⭐⭐⭐⭐ |
| BSL | ✅ Yes | ⚠️ Delayed | ⚠️ Time-limited | ⭐⭐⭐ |

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

## IP Protection Strategy

### Phase 1 (Now - MVP): Elastic License 2.0
- Source-available on GitHub
- Prevent SaaS competition
- Build community trust
- Validate product-market fit

### Phase 2 (Month 6 - Traction): Commercial Licensing
- Self-hosted: Free (Elastic License)
- Enterprise features: Commercial licenses ($5K-$50K/year)
  - SSO/SAML integration
  - Multi-tenancy
  - Priority support
  - SLA guarantees
  - Custom integrations

### Phase 3 (Month 12 - Scale): Official SaaS
- Self-hosted: Free (Elastic License)
- Cloud hosted: Exclusive offering ($49-$499/month tiers)
- Enterprise: Custom pricing + white-label options
- No competition risk (license prevents third-party SaaS)

### Revenue Model Options

1. **Open Core Model**:
   - Basic features: Free (Elastic License)
   - Advanced features: Paid license
   - Examples: GitLab, Terraform

2. **SaaS Exclusive**:
   - Self-hosted: Free
   - Cloud version: Only you can offer it
   - Examples: Elastic Cloud, MongoDB Atlas

3. **Dual Licensing**:
   - Elastic License 2.0 for most users
   - MIT/Apache for paying enterprise customers (remove restrictions)
   - Examples: MySQL, Qt

---

## Checklist Before First Commit

- [x] Verify multi-agent-workflow license → **UNLICENSED** (see NOTICE)
- [x] Verify claude-code-proxy license → **UNLICENSED** (see NOTICE)
- [x] Create `LICENSE` file with Elastic License 2.0
- [x] Create `NOTICE` file documenting unlicensed dependencies
- [ ] Add "License: Elastic-2.0" badge to README.md
- [ ] Add licensing section to README.md
- [ ] Update package.json with `"license": "Elastic-2.0"`

---

## Summary

**Chosen License**: Elastic License 2.0

**Key Benefits:**
- ✅ Source-available (GitHub-friendly, builds trust)
- ✅ Prevents SaaS competition (only you can offer cloud version)
- ✅ Allows users to view, modify, and use internally
- ✅ Protects commercial opportunities
- ✅ Patent protection included
- ✅ Industry-proven (Elasticsearch, Kibana, etc.)

**Trade-offs:**
- ⚠️ Slightly lower GitHub star potential vs MIT (but still 4/5 stars)
- ⚠️ Some enterprises may prefer MIT/Apache for procurement
- ⚠️ Cannot be used in other open-source projects that require permissive licenses

**Upstream Dependency Risk:**
- ⚠️ multi-agent-workflow: UNLICENSED (see NOTICE file)
- ⚠️ claude-code-proxy: UNLICENSED (see NOTICE file)
- ✅ Mitigation: Reference only, prepared to rewrite if legal issues arise

**Commercialization Path:**
1. **Now**: Free self-hosted (Elastic License 2.0)
2. **6 months**: Add paid enterprise features
3. **12 months**: Launch exclusive SaaS offering
4. **18+ months**: White-label & custom licensing

**Why This Works:**
- Elastic (the company) uses this model successfully
- Prevents AWS/Azure from offering competing managed service
- You control the cloud offering exclusively
- Still builds community (code is visible and forkable)
- Maximum long-term revenue potential
