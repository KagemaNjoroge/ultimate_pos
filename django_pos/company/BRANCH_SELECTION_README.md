# Branch Selection Feature Documentation

## Overview

The branch selection feature allows users to select and switch between different company branches within the Ultimate POS system. This feature includes automatic branch selection persistence, search functionality, and time-based greetings.

## Components

### 1. Templates

- **`select_branch.html`**: Standalone branch selection page with modern UI
  - Time-based greeting (Good Morning/Afternoon/Evening/Night)
  - Search functionality to filter branches
  - Local storage integration for branch persistence
  - Responsive design with smooth animations

### 2. Views

- **`select_current_branch`**: Main view for branch selection
  - Handles GET requests to display the selection page
  - Handles POST requests to save branch selection
  - Automatically creates default branch if none exist
- **`switch_branch`**: AJAX endpoint for quick branch switching
  - Allows switching branches without full page reload
  - Returns JSON response with branch information

### 3. Middleware

- **`BranchSelectionMiddleware`**: Ensures users have selected a branch
  - Redirects to branch selection page if no branch is selected
  - Exempts authentication and setup URLs
  - Handles cases where no branches exist

### 4. Context Processors

- **`current_branch_context`**: Adds current branch info to all templates
  - Makes branch information available globally
  - Handles invalid branch sessions

### 5. Utilities

- **`branch_utils.py`**: Helper functions for branch management
  - `get_current_branch()`: Get current branch from session
  - `set_current_branch()`: Set current branch in session
  - `clear_current_branch()`: Clear branch from session
  - `ensure_default_branch()`: Create default branch if needed

### 6. JavaScript Components

- **`branch-selector.js`**: Branch selection page functionality
  - Time-based greeting generation
  - Local storage management
  - Search and filtering
  - Branch selection handling
- **`branch-manager.js`**: Global branch management utilities
  - AJAX branch switching
  - Branch information display updates
  - Dropdown initialization

## Features

### 1. Automatic Branch Selection

- Remembers previously selected branch in localStorage
- Auto-selects saved branch on page load
- Displays notification when auto-selecting

### 2. Search Functionality

- Real-time search through branch names, addresses, and phone numbers
- Clear search with Escape key
- No results message with clear search option

### 3. Time-Based Greeting

- Dynamic greeting based on current time:
  - 5-12: Good Morning! 🌅
  - 12-17: Good Afternoon! ☀️
  - 17-21: Good Evening! 🌇
  - 21-5: Good Night! 🌙

### 4. Keyboard Navigation

- Arrow keys to navigate between branches
- Enter to submit selection
- Escape to clear search

### 5. Responsive Design

- Mobile-friendly layout
- Touch-friendly interface
- Smooth animations and transitions

## Usage

### Setup

1. Add middleware to `settings.py`:

   ```python
   MIDDLEWARE = [
       # ... other middleware
       "company.middleware.BranchSelectionMiddleware",
   ]
   ```

2. Add context processor to `settings.py`:
   ```python
   TEMPLATES = [{
       'OPTIONS': {
           'context_processors': [
               # ... other processors
               "company.context_processors.current_branch_context",
           ],
       },
   }]
   ```

### URL Configuration

```python
path("select_current_branch/", select_current_branch, name="select_current_branch"),
path("switch_branch/", switch_branch, name="switch_branch"),
```

### JavaScript Usage

```javascript
// Switch branch programmatically
BranchManager.switchBranch(branchId, onSuccess, onError);

// Get current branch
const currentBranch = BranchManager.getCurrentBranch();

// Update branch display
BranchManager.updateBranchDisplay(branchData);
```

### Template Usage

```html
<!-- Display current branch name -->
<span class="current-branch-name">{{ current_branch_name }}</span>

<!-- Branch selector dropdown -->
<div class="branch-selector-dropdown"></div>
```

## Local Storage

The system uses localStorage to persist branch selection:

```javascript
// Storage key
const storageKey = 'ultimatepos_current_branch';

// Stored data structure
{
    id: 1,
    name: "Main Branch",
    address: "123 Main St",
    phone: "+1234567890",
    timestamp: 1672531200000
}
```

## Security

- CSRF protection on all POST requests
- User authentication required
- Branch access validation
- Session-based branch tracking

## Error Handling

- Invalid branch selections are handled gracefully
- Network errors show user-friendly messages
- Automatic cleanup of invalid session data
- Fallback to branch selection page when needed

## Styling

The branch selection page includes:

- Modern gradient backgrounds
- Card-based layout
- Smooth hover effects
- Loading states
- Responsive breakpoints
- Accessible form controls

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript required for full functionality
- Graceful fallback for basic form submission
