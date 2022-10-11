lang = {
    search: {
        resultsFound: "Found",
        noResultsFound: "No results found"
    }
}

function pluralizeResults(size) {
    if (size == 1) {
        return "result";
    } else {
        return "results";
    }
}