// Global search options
var theme_static_search = JSON.parse(
  '{"ignoreLocation": true, "keys": ["title", "text"], "limit": 10, "min_chars_for_search": 1, "shouldSort": "True", "threshold": 0.5, "useExtendedSearch": "True"}',
);
var theme_limit = "10";
var min_chars_for_search = "1";

// Configure RequireJS
require.config({
  paths: {
    fuse: "https://cdn.jsdelivr.net/npm/fuse.js@6.4.6/dist/fuse.min",
  },
});

// Main script for search functionality
require(["fuse"], function (Fuse) {
  let fuseInstance;
  let searchData = [];

  // Initialize Fuse.js with search data and options
  function initializeFuse(data) {
    const fuseOptions = theme_static_search;
    fuseInstance = new Fuse(data, fuseOptions);
    searchData = data; // Save the search data for later use
  }

  // Perform search with Fuse.js
  function performSearch(query) {
    const results = fuseInstance.search(query, {
      limit: parseInt(theme_limit),
    });
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "";

    if (results.length === 0) {
      displayNoResultsMessage(resultsContainer);
      return;
    }

    // Show the results container if there's a query
    if (query === "") {
      resultsContainer.style.display = "none";
      return;
    }
    resultsContainer.style.display = "block";

    // Populate results
    results.forEach((result) => {
      const { title, text, href } = result.item;
      const item = createResultItem(title, text, href, query);
      resultsContainer.appendChild(item);
    });
  }

  // Display "No matched documents" message
  function displayNoResultsMessage(container) {
    const noResultsMessage = document.createElement("div");
    noResultsMessage.className = "no-results";
    noResultsMessage.textContent = "No matched documents";
    container.appendChild(noResultsMessage);
  }

  // Create and return a result item
  function createResultItem(title, text, href, query) {
    const item = document.createElement("div");
    item.className = "result-item";

    const highlightedTitle = highlightTerms(title, query);
    const highlightedText = highlightTerms(text, query);

    item.innerHTML = `
        <div class="result-title">${highlightedTitle}</div>
        <div class="result-text">${highlightedText}</div>
      `;
    item.setAttribute("data-href", href);

    // Navigate to the result's href on click
    item.addEventListener("click", () => navigateToHref(href));
    return item;
  }

  // Highlight matching terms in search results
  function highlightTerms(text, query) {
    if (!query.trim()) return text;
    const words = query.trim().split(/\s+/);
    const escapedWords = words.map((word) =>
      word.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&"),
    );
    const regex = new RegExp(`(${escapedWords.join("|")})`, "gi");
    return text.replace(regex, '<span class="highlight">$1</span>');
  }

  // Navigate to the href
  function navigateToHref(href) {
    const baseUrl = window.location.origin;
    const relativeUrl = href.startsWith("/") ? href : `/${href}`;
    window.location.href = new URL(relativeUrl, baseUrl).href;
  }

  // Event listeners
  const searchBox = document.querySelector(".bd-search input");

  // Handle input in the search box
  searchBox.addEventListener("input", function () {
    const query = this.value.trim();
    if (query.length < parseInt(min_chars_for_search)) {
      document.getElementById("results").innerHTML = "";
      return;
    }
    performSearch(query);
  });

  // Handle Enter key press in the search box
  searchBox.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      const firstResult = document.querySelector(".result-item");
      if (firstResult) {
        navigateToHref(firstResult.getAttribute("data-href"));
      }
      event.preventDefault();
    }
  });

  // Fetch search data and initialize Fuse.js
  fetch("search.json")
    .then((response) =>
      response.ok
        ? response.json()
        : Promise.reject("Error: " + response.statusText),
    )
    .then((data) => initializeFuse(data))
    .catch((error) => console.error("Fetch operation failed:", error));
});
