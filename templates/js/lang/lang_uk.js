lang = {
    search: {
        resultsFound: "Знайдено",
        noResultsFound: "Не знайдено жодного результату"
    }
}

function pluralizeResults(size) {
    var lastDigit = size % 10;
    if (lastDigit == 1) {
        return "результат";
    } else if (lastDigit > 1 && lastDigit < 5) {
        return "результати";
    } else if (lastDigit == 0 || lastDigit > 4) {
        return "результатів"
    }
}