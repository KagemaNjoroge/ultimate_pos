/**
 * Branch Selection Functionality
 * Handles branch selection, local storage, and search functionality
 */

class BranchSelector {
  constructor() {
    this.storageKey = "ultimatepos_current_branch";
    this.searchInput = $("#branch-search");
    this.branchItems = $(".branch-item");
    this.continueBtn = $("#continue-btn");
    this.branchForm = $("#branch-form");

    this.init();
  }

  init() {
    this.setTimeBasedGreeting();
    this.loadSavedBranch();
    this.bindEvents();
    this.autoFocusSearch();
  }

  bindEvents() {
    // Branch selection
    this.branchItems.on("click", (e) => {
      this.selectBranch($(e.currentTarget));
    });

    // Search functionality
    this.searchInput.on("input", (e) => {
      this.filterBranches($(e.target).val());
    });

    // Clear search on Escape
    this.searchInput.on("keydown", (e) => {
      if (e.key === "Escape") {
        this.clearSearch();
      }
    });

    // Form submission
    this.branchForm.on("submit", (e) => {
      const selectedBranch = $(".branch-item.selected");
      if (selectedBranch.length > 0) {
        this.saveBranchToLocalStorage(selectedBranch);
        toastr.success("Branch selected successfully!");
      }
    });
  }

  setTimeBasedGreeting() {
    const now = new Date();
    const hour = now.getHours();
    let greeting, icon;

    if (hour >= 5 && hour < 12) {
      greeting = "Good Morning!";
      icon = "🌅";
    } else if (hour >= 12 && hour < 17) {
      greeting = "Good Afternoon!";
      icon = "☀️";
    } else if (hour >= 17 && hour < 21) {
      greeting = "Good Evening!";
      icon = "🌇";
    } else {
      greeting = "Good Night!";
      icon = "🌙";
    }

    $("#greeting-text").text(greeting);
    $("#greeting-icon").text(icon);
  }

  selectBranch($branchItem) {
    // Remove selection from all branches
    this.branchItems.removeClass("selected");
    $(".branch-radio").prop("checked", false);

    // Select the clicked branch
    $branchItem.addClass("selected");
    $branchItem.find(".branch-radio").prop("checked", true);

    // Enable continue button
    this.continueBtn.prop("disabled", false);

    // Add visual feedback
    $branchItem.velocity("callout.pulse", { duration: 300 });
  }

  saveBranchToLocalStorage($branchItem) {
    const branchData = {
      id: $branchItem.data("branch-id"),
      name: $branchItem.data("branch-name"),
      address: $branchItem.data("branch-address"),
      phone: $branchItem.data("branch-phone"),
      timestamp: new Date().getTime(),
    };

    try {
      localStorage.setItem(this.storageKey, JSON.stringify(branchData));
    } catch (error) {
      console.warn("Failed to save branch to localStorage:", error);
    }
  }

  loadSavedBranch() {
    const savedBranch = localStorage.getItem(this.storageKey);

    if (savedBranch) {
      try {
        const branchData = JSON.parse(savedBranch);
        const $savedBranchItem = $(
          `.branch-item[data-branch-id="${branchData.id}"]`
        );

        if ($savedBranchItem.length > 0) {
          this.selectBranch($savedBranchItem);
          toastr.info(
            `Previously selected: ${branchData.name}`,
            "Auto-selected Branch",
            {
              timeOut: 3000,
              extendedTimeOut: 1000,
            }
          );
        } else {
          // Branch no longer exists, clear from storage
          this.clearSavedBranch();
        }
      } catch (error) {
        console.warn("Error loading saved branch:", error);
        this.clearSavedBranch();
      }
    }
  }

  clearSavedBranch() {
    try {
      localStorage.removeItem(this.storageKey);
    } catch (error) {
      console.warn("Failed to clear saved branch:", error);
    }
  }

  filterBranches(searchTerm) {
    const term = searchTerm.toLowerCase().trim();
    let visibleCount = 0;

    this.branchItems.each((index, element) => {
      const $item = $(element);
      const branchName = ($item.data("branch-name") || "").toLowerCase();
      const branchAddress = ($item.data("branch-address") || "").toLowerCase();
      const branchPhone = ($item.data("branch-phone") || "").toLowerCase();

      const matches =
        branchName.includes(term) ||
        branchAddress.includes(term) ||
        branchPhone.includes(term);

      if (matches || term === "") {
        $item.show();
        visibleCount++;
      } else {
        $item.hide();
      }
    });

    this.toggleNoResultsMessage(visibleCount === 0 && term !== "");
  }

  toggleNoResultsMessage(show) {
    const existingMessage = $("#no-search-results");

    if (show) {
      if (existingMessage.length === 0) {
        const noResultsHtml = `
                    <div id="no-search-results" class="no-branches">
                        <i class="ti ti-search-off" style="font-size: 3rem; color: #ccc; margin-bottom: 15px;"></i>
                        <h5>No branches found</h5>
                        <p>Try adjusting your search terms or <a href="#" id="clear-search-link">clear search</a>.</p>
                    </div>
                `;
        $("#branches-list").append(noResultsHtml);

        // Bind clear search event
        $("#clear-search-link").on("click", (e) => {
          e.preventDefault();
          this.clearSearch();
        });
      }
    } else {
      existingMessage.remove();
    }
  }

  clearSearch() {
    this.searchInput.val("");
    this.filterBranches("");
    this.autoFocusSearch();
  }

  autoFocusSearch() {
    setTimeout(() => {
      this.searchInput.focus();
    }, 100);
  }

  // Public methods for external access
  getCurrentSelection() {
    const selectedBranch = $(".branch-item.selected");
    if (selectedBranch.length > 0) {
      return {
        id: selectedBranch.data("branch-id"),
        name: selectedBranch.data("branch-name"),
        address: selectedBranch.data("branch-address"),
        phone: selectedBranch.data("branch-phone"),
      };
    }
    return null;
  }

  selectBranchById(branchId) {
    const $branch = $(`.branch-item[data-branch-id="${branchId}"]`);
    if ($branch.length > 0) {
      this.selectBranch($branch);
      return true;
    }
    return false;
  }
}

// Initialize branch selector when document is ready
$(document).ready(function () {
  window.branchSelector = new BranchSelector();

  // Add keyboard shortcuts
  $(document).on("keydown", function (e) {
    // Enter key to submit if branch is selected
    if (e.key === "Enter" && !$("#continue-btn").prop("disabled")) {
      e.preventDefault();
      $("#branch-form").submit();
    }

    // Arrow navigation for branches
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      navigateBranches(e.key === "ArrowDown");
    }
  });

  function navigateBranches(down) {
    const visibleBranches = $(".branch-item:visible");
    const currentIndex = visibleBranches.index($(".branch-item.selected"));
    let newIndex;

    if (down) {
      newIndex =
        currentIndex < visibleBranches.length - 1 ? currentIndex + 1 : 0;
    } else {
      newIndex =
        currentIndex > 0 ? currentIndex - 1 : visibleBranches.length - 1;
    }

    if (newIndex >= 0 && newIndex < visibleBranches.length) {
      window.branchSelector.selectBranch($(visibleBranches[newIndex]));

      // Scroll into view
      visibleBranches[newIndex].scrollIntoView({
        behavior: "smooth",
        block: "nearest",
      });
    }
  }
});
