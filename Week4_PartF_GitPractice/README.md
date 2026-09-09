# Week 4 — Part F: Git & GitHub Level Up

**Author:** Asiya  
**Project:** Professional Git Workflow, Merge Conflict Resolution & Branch Protection

## Objectives
1. Understand and resolve manual merge conflicts caused by divergent branch histories.
2. Establish GitHub branch protection rules on `main`.
3. Standardize collaborative Pull Requests with `.github/PULL_REQUEST_TEMPLATE.md`.

---

## Deliberate Merge Conflict Exercise Walkthrough

### 1. The Scenario
Two developers modify the exact same line in `README.md` concurrently on separate branches:
- Branch `practice/conflict-a`
- Branch `practice/conflict-b`

### 2. Conflict Anatomy
When attempting to merge `practice/conflict-b` into `main` after `practice/conflict-a` was already merged:
```markdown
<<<<<<< HEAD
A simple library management demo built during the internship.
=======
A library management app built by two interns learning .NET, Angular, and AI.
>>>>>>> practice/conflict-b
```

### 3. Resolution Steps
1. Open the conflicted file.
2. Manually review both changes and synthesize them into the finalized accurate text:
   ```markdown
   A secure, full-stack library management application built with ASP.NET Core, Angular, and FastAPI AI microservices.
   ```
3. Remove all Git conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
4. Stage the resolved file and commit:
   ```bash
   git add README.md
   git commit -m "fix(git): resolve merge conflict in README.md"
   ```

---

## Branch Protection Rules Setup
- Under GitHub Repository -> **Settings** -> **Branches**:
  1. Add rule for branch pattern `main`.
  2. Check **Require a pull request before merging**.
  3. Check **Require approvals** (minimum 1 approval).
  4. Ensure no direct pushes are permitted to `main`.
