# Overview of PyLith Code

## PyLith design

- Python/C++
- SWIG -> pybind11
- PyLith pplication flow

## Code layout

- Directory structure
- Application
- Problem
- Physics and finite-element objects
- Materials
- Boundary conditions and faults
- Mesh importing 
- Output

### Development container

- High-level organization
- Directory structure

## PETSc finite-element implementation

- Terminology
- DMPlex
  - Points, etc;
  - Numbering
- PetscSection and PetscVec and pylith::topology::Field
- Integration
- Projection
- Auxiliary fields

## Documentation

- MyST -> html via Sphinx
- Layout
- Building documentation
- Viewing documentation
- MyST quick reference

## Testing overview

- libtests (libsrc)
- mmstests (libsrc)
- pytests (libsrc+SWIG)
- full-scale (full stack)

## Building

- overview
- autoconf (configure.ac, Makefile.am)
- lib
- modules
- Python
- CLI (terminal)
- VS Code shortcuts

## Running tests

- Overview (Catch2, unittest)
- Building libtests and mmstests
- Running tests CLI
- VS Code shortcuts

## Git workflow

- Forking and branching workflow
  - Overview
  - Adding a feature
- Tasks
  - Updating your local `main` branch
  - Creating a feature branch
  - Staging, committing, and pushing changes
  - Creating a pull request
  - Keeping a feature branch in sync with upstream `main`
  - Adding remots for accessing other PyLith forks

## Adding a feature workflow

### Prerequisites:

- Local dev environment
- Clone of repository

Steps

1. Update `main`
2. Create feature branch
3. Implement feature
4. Build
5. Implement test
6. Build test
7. Run/debug test
8. Document feature
9. Create pull request
10. Pull request is reviewed
11. Revise pull request
12. Pull request is merged

## Using VS Code

- Intro
  - Open folder at top-level of repository (.vscode)
  - Tour
    - Explorer
    - Search
    - Source control
    - Extensions
    - Debug
    - Tests
    - Python virtual environment
    - Git branch
- Search
- Formatting code
  - C++
  - Python
  - Markdown
- Understanding highlighting
  - Typos
  - Warnings and errors
- Extensions
  - GitGraph 
