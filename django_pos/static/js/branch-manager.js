/**
 * Global Branch Management Utilities
 * Provides functionality to switch branches from anywhere in the application
 */

window.BranchManager = {
  /**
   * Switch to a different branch via AJAX
   * @param {number} branchId - The ID of the branch to switch to
   * @param {function} onSuccess - Callback function on successful switch
   * @param {function} onError - Callback function on error
   */
  switchBranch: function (branchId, onSuccess, onError) {
    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!this.crossDomain) {
          xhr.setRequestHeader(
            "X-CSRFToken",
            $("[name=csrfmiddlewaretoken]").val()
          );
        }
      },
    });

    $.post("/company/switch_branch/", {
      branch_id: branchId,
    })
      .done(function (data) {
        if (data.success) {
          // Update localStorage with new branch info
          const branchData = {
            id: data.branch.id,
            name: data.branch.name,
            address: data.branch.address,
            phone: data.branch.phone,
            timestamp: new Date().getTime(),
          };
          localStorage.setItem(
            "ultimatepos_current_branch",
            JSON.stringify(branchData)
          );

          // Show success message
          if (typeof toastr !== "undefined") {
            toastr.success(data.message);
          }

          // Call success callback
          if (typeof onSuccess === "function") {
            onSuccess(data.branch);
          } else {
            // Default behavior: reload the page
            window.location.reload();
          }
        } else {
          if (typeof toastr !== "undefined") {
            toastr.error(data.message);
          }
          if (typeof onError === "function") {
            onError(data.message);
          }
        }
      })
      .fail(function (xhr, status, error) {
        const errorMessage = "Failed to switch branch. Please try again.";
        if (typeof toastr !== "undefined") {
          toastr.error(errorMessage);
        }
        if (typeof onError === "function") {
          onError(errorMessage);
        }
      });
  },

  /**
   * Get current branch information from localStorage
   * @returns {object|null} Branch data or null if not found
   */
  getCurrentBranch: function () {
    try {
      const branchData = localStorage.getItem("ultimatepos_current_branch");
      return branchData ? JSON.parse(branchData) : null;
    } catch (error) {
      console.warn("Error reading current branch from localStorage:", error);
      return null;
    }
  },

  /**
   * Update current branch display in the UI
   * @param {object} branchData - Branch data object
   */
  updateBranchDisplay: function (branchData) {
    // Update any elements with class 'current-branch-name'
    $(".current-branch-name").text(branchData.name);

    // Update any elements with class 'current-branch-address'
    $(".current-branch-address").text(branchData.address || "");

    // Update any elements with class 'current-branch-phone'
    $(".current-branch-phone").text(branchData.phone || "");

    // Update page title if needed
    if (branchData.name) {
      document.title = document.title.replace(
        /- .+ Branch/,
        `- ${branchData.name}`
      );
    }
  },

  /**
   * Initialize branch dropdown for quick switching
   * @param {string} dropdownSelector - CSS selector for the dropdown container
   */
  initBranchDropdown: function (dropdownSelector) {
    const $dropdown = $(dropdownSelector);
    if ($dropdown.length === 0) return;

    // Fetch available branches
    this.loadBranchesForDropdown($dropdown);
  },

  /**
   * Load branches for dropdown menu
   * @param {jQuery} $dropdown - jQuery object of the dropdown container
   */
  loadBranchesForDropdown: function ($dropdown) {
    // This would typically make an API call to get available branches
    // For now, we'll use a simple implementation

    const currentBranch = this.getCurrentBranch();
    const dropdownHtml = `
            <div class="dropdown">
                <button class="btn btn-outline-secondary dropdown-toggle" type="button" id="branchDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="ti ti-building"></i> ${
                      currentBranch ? currentBranch.name : "Select Branch"
                    }
                </button>
                <ul class="dropdown-menu" aria-labelledby="branchDropdown">
                    <li><h6 class="dropdown-header">Switch Branch</h6></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="/company/select_current_branch/">
                        <i class="ti ti-list"></i> View All Branches
                    </a></li>
                </ul>
            </div>
        `;

    $dropdown.html(dropdownHtml);
  },

  /**
   * Format branch name for display
   * @param {string} branchName - Original branch name
   * @param {boolean} isHeadquarter - Whether this is the headquarters
   * @returns {string} Formatted branch name
   */
  formatBranchName: function (branchName, isHeadquarter) {
    return isHeadquarter ? `${branchName} (HQ)` : branchName;
  },

  /**
   * Check if branch selection is required
   * @returns {boolean} True if branch selection is required
   */
  isBranchSelectionRequired: function () {
    return this.getCurrentBranch() === null;
  },

  /**
   * Redirect to branch selection page if no branch is selected
   */
  enforcebranchSelection: function () {
    if (this.isBranchSelectionRequired()) {
      window.location.href = "/company/select_current_branch/";
    }
  },
};

// Auto-initialize on document ready
$(document).ready(function () {
  // Initialize branch dropdown if it exists
  BranchManager.initBranchDropdown(".branch-selector-dropdown");

  // Update branch display on page load
  const currentBranch = BranchManager.getCurrentBranch();
  if (currentBranch) {
    BranchManager.updateBranchDisplay(currentBranch);
  }
});
