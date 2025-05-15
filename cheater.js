let wordList = [];
let cheater;
let guessCount = 0; // Keep track of the number of guesses

class Cheater {
  constructor(wordlist) {
    this.guessed = [];

    // Convert all words to uppercase first
    const uppercaseWordlist = wordlist.map((word) => word.toUpperCase());

    // Use provided wordlist array directly (now all uppercase)

    this.clean_words = [...uppercaseWordlist];
    this.salty_words = [...uppercaseWordlist];

    // Create letter frequency counts (equivalent to numpy zeros)
    this.counts = Array(26).fill(0);
    for (let word of this.clean_words) {
      for (let letter of word) {
        this.counts[letter.charCodeAt(0) - 65] += 1;
      }
    }

    // Count letters by position
    let counts_by_position = Array(26)
      .fill()
      .map(() => Array(5).fill(0));
    for (let word of this.clean_words) {
      for (let position = 0; position < word.length; position++) {
        let letter = word[position];
        let index = letter.charCodeAt(0) - 65;
        // Still include a safety check just in case
        if (index >= 0 && index < 26) {
          counts_by_position[index][position] += 1;
        }
      }
    }

    // Calculate medians for each position
    let medians = [];
    for (let pos = 0; pos < 5; pos++) {
      let positionValues = [];
      for (let i = 0; i < 26; i++) {
        positionValues.push(counts_by_position[i][pos]);
      }
      medians.push(this.median(positionValues));
    }

    // Calculate scores by position
    let scores_by_pos = Array(26)
      .fill()
      .map(() => Array(5).fill(0));
    for (let i = 0; i < scores_by_pos.length; i++) {
      for (let j = 0; j < scores_by_pos[i].length; j++) {
        scores_by_pos[i][j] = counts_by_position[i][j] / medians[j];
      }
    }

    // Calculate word scores
    this.scores = Array(this.clean_words.length).fill(0);
    for (let i = 0; i < this.clean_words.length; i++) {
      let word = this.clean_words[i];
      for (let position = 0; position < word.length; position++) {
        let letter = word[position];
        this.scores[i] += scores_by_pos[letter.charCodeAt(0) - 65][position];
      }
    }
    this.salty_scores = [...this.scores]; // Copy scores array
  }

  // Helper method to calculate median
  median(values) {
    if (values.length === 0) return 0;

    values.sort((a, b) => a - b);

    const half = Math.floor(values.length / 2);

    if (values.length % 2) {
      return values[half];
    }

    return (values[half - 1] + values[half]) / 2.0;
  }

  get_clean_candidates() {
    let doomed = [];
    for (let i = 0; i < this.clean_words.length; i++) {
      let word = this.clean_words[i];
      for (let letter of word) {
        if (word.split(letter).length - 1 > 1) {
          // Count occurrences
          doomed.push(i);
          break;
        }
      }
    }

    // Remove doomed words
    let words = this.clean_words.filter((_, index) => !doomed.includes(index));
    let scores = this.scores.filter((_, index) => !doomed.includes(index));

    return getCandidates(words, scores);
  }

  get_salty_candidates() {
    let doomed = [];
    for (let i = 0; i < this.salty_words.length; i++) {
      let word = this.salty_words[i];
      for (let guess of this.guessed) {
        if (word.includes(guess)) {
          doomed.push(i);
          break;
        }
      }
    }

    // Remove doomed words
    let words = this.salty_words.filter((_, index) => !doomed.includes(index));
    let scores = this.salty_scores.filter(
      (_, index) => !doomed.includes(index)
    );

    // Now filter words with duplicate letters
    let secondDoomed = [];
    for (let i = 0; i < words.length; i++) {
      let word = words[i];
      for (let letter of word) {
        if (word.split(letter).length - 1 > 1) {
          // Count occurrences
          secondDoomed.push(i);
          break;
        }
      }
    }

    words = words.filter((_, index) => !secondDoomed.includes(index));
    scores = scores.filter((_, index) => !secondDoomed.includes(index));

    return getCandidates(words, scores);
  }

  print_status() {
    console.log(`${this.clean_words.length} possible words remain`);
    let a = getCandidates(this.clean_words, this.scores);
    let b = this.get_clean_candidates();
    let c = this.get_salty_candidates();
    let d = "";

    console.log(`Most likely: ${a}`);
    console.log(`No doubles: ${b}`);
    console.log(`New letters: ${c}`);

    if (c.trim().length > 1) {
      d = c.substring(0, 6);
    } else if (b.trim().length > 1) {
      d = b.substring(0, 6);
    } else if (a.trim().length > 1) {
      d = a.substring(0, 6);
    }

    console.log(`Best guess: ${d}`);
    return d.trim();
  }

  rule_out_letter(letter) {
    // Add the guessed letter
    // Assumes 'this.guessed' is an array
    this.guessed.push(letter);

    // --- Handle clean words and scores ---
    const newCleanWords = [];
    const newScores = [];

    // Iterate through the current words and scores
    for (let i = 0; i < this.clean_words.length; i++) {
      const word = this.clean_words[i];
      const score = this.scores[i];

      // Keep the word and its score ONLY if the word does NOT contain the letter
      if (!word.includes(letter)) {
        newCleanWords.push(word);
        newScores.push(score);
      }
    }

    // Replace the old arrays with the new ones that exclude words containing the letter
    this.clean_words = newCleanWords;
    this.scores = newScores;

    // --- Handle salty words and scores ---
    const newSaltyWords = [];
    const newSaltyScores = [];

    // Iterate through the current salty words and scores
    for (let i = 0; i < this.salty_words.length; i++) {
      const word = this.salty_words[i];
      const score = this.salty_scores[i];

      // Keep the word and its score ONLY if the word does NOT contain the letter
      if (!word.includes(letter)) {
        newSaltyWords.push(word);
        newSaltyScores.push(score);
      }
    }

    // Replace the old arrays with the new ones that exclude salty words containing the letter
    this.salty_words = newSaltyWords;
    this.salty_scores = newSaltyScores;
  }

  require_letter(letter) {
    this.guessed.push(letter);

    // Create new arrays by filtering the old ones
    // Keep only elements where the word contains the letter
    const newCleanWords = [];
    const newScores = [];

    for (let i = 0; i < this.clean_words.length; i++) {
      const word = this.clean_words[i];
      const score = this.scores[i];

      // Keep the word and score if the word includes the required letter
      if (word.includes(letter)) {
        newCleanWords.push(word);
        newScores.push(score);
      }
    }

    // Replace the old arrays with the filtered ones
    this.clean_words = newCleanWords;
    this.scores = newScores;
  }

  // Helper method to filter paired arrays based on a condition in the first array
  // Keeps the pair if the character at 'position' is NOT the specified letter
  _filterOutLetterAtPosition(words, scores, letter, position) {
    const newWords = [];
    const newScores = [];
    for (let i = 0; i < words.length; i++) {
      const word = words[i];
      const score = scores[i];

      // Keep the word and its score if the character at 'position' is NOT the specified letter
      // Added safety checks for word existence, type, and length.
      if (
        word &&
        typeof word === "string" &&
        word.length > position &&
        word[position] !== letter
      ) {
        newWords.push(word);
        newScores.push(score);
      }
    }
    return [newWords, newScores];
  }

  rule_out_letter_at_position(letter, position) {
    // Add the guessed letter to the list
    // Assumes 'this.guessed' is an array
    this.guessed.push(letter);

    // Process clean_words and scores
    // Use the helper function and array destructuring to update the properties
    [this.clean_words, this.scores] = this._filterOutLetterAtPosition(
      this.clean_words,
      this.scores,
      letter,
      position
    );

    // Process salty_words and salty_scores
    // Use the helper function again for the salty pair
    [this.salty_words, this.salty_scores] = this._filterOutLetterAtPosition(
      this.salty_words,
      this.salty_scores,
      letter,
      position
    );
  }

  require_letter_at_position(letter, position) {
    // Add the guessed letter to the list
    // Assumes 'this.guessed' is an array
    this.guessed.push(letter);

    // Create new arrays to hold the words and scores that meet the criteria
    const newCleanWords = [];
    const newScores = [];

    // Iterate through the current clean words and scores
    for (let i = 0; i < this.clean_words.length; i++) {
      const word = this.clean_words[i];
      const score = this.scores[i];

      // Check if the word is valid and has a character at the specified position
      // and if that character matches the required letter.
      // We KEEP the word and score if the character at 'position' IS the required letter.
      // Added safety checks for word existence and length.
      if (
        word &&
        typeof word === "string" &&
        word.length > position &&
        word[position] === letter
      ) {
        newCleanWords.push(word);
        newScores.push(score);
      }
    }

    // Replace the old arrays with the new, filtered arrays
    this.clean_words = newCleanWords;
    this.scores = newScores;

    // Note: Your Python function only modified self.clean_words and self.scores.
    // If you had corresponding salty_words and salty_scores that needed the same logic,
    // you would add a similar block here.
  }
}

// Including the getCandidates function we translated earlier
function getCandidates(words, scores) {
  let numWords = 10;
  if (words.length < 10) {
    numWords = words.length;
  }

  // Create array of indices and scores
  let indexScorePairs = [];
  for (let i = 0; i < scores.length; i++) {
    indexScorePairs.push([i, scores[i]]);
  }

  // Sort by score (descending)
  indexScorePairs.sort((a, b) => b[1] - a[1]);

  // Take top numWords
  indexScorePairs = indexScorePairs.slice(0, numWords);

  // Sort by index
  indexScorePairs.sort((a, b) => a[0] - b[0]);

  // Get top words
  let topWords = [];
  for (let i = 0; i < numWords; i++) {
    topWords.push(words[indexScorePairs[i][0]]);
  }

  // Reverse the array (equivalent to Python's [::-1])
  topWords.reverse();

  // Create output string
  let out = "";
  for (let word of topWords) {
    out += ` ${word}`;
  }

  return out;
}

const wordListDiv = document.getElementById("wordList");
const startButton = document.getElementById("startButton");
const mainContent = document.getElementById("mainContent");

function updateOptions() {
  wordListDiv.innerHTML =
    `<h2>Remaining Options: ${wordList.length}</h2><ul>` +
    wordList.map((word) => `<li>${word}</li>`).join("") +
    "</ul>";
  wordListDiv.style.display = "block";
}

window.onload = function () {
  fetch(
    "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/c46f451920d5cf6326d550fb2d6abb1642717852/wordle-answers-alphabetical.txt"
  )
    .then((response) => response.text())
    .then((data) => {
      wordList = data.split("\n");
      console.log(wordList);
      cheater = new Cheater(wordList);
      updateOptions();
      startButton.style.display = "block";
    })
    .catch((error) => console.error("Error fetching word list:", error));
};

startButton.onclick = function () {
  startButton.style.display = "none";
  printAndProcessGuess(); // Initial guess
};

function printAndProcessGuess() {
  const guessDiv = document.createElement("div");
  guessDiv.style.marginBottom = "10px";
  let guess = cheater.print_status();
  for (let index = 0; index < guess.length; index++) {
    const letterbox = document.createElement("div");
    letterbox.className = "letterbox";
    letterbox.textContent = guess.charAt(index);
    letterbox.dataset.colorIndex = 0;
    letterbox.addEventListener("click", cycleLetterboxColor);
    guessDiv.appendChild(letterbox);
  }
  const processButton = document.createElement("button");
  processButton.textContent = `Process Guess ${++guessCount}`; // Increment and display
  processButton.disabled = true;
  processButton.addEventListener("click", processGuess);
  guessDiv.appendChild(processButton);
  mainContent.appendChild(guessDiv);
  mainContent.style.display = "block";
}

function cycleLetterboxColor() {
  const colors = ["#333", "grey", "yellow", "green"];
  let colorIndex = parseInt(this.dataset.colorIndex) || 0;
  colorIndex = (colorIndex + 1) % colors.length;
  this.style.backgroundColor = colors[colorIndex];
  this.dataset.colorIndex = colorIndex;

  const letterBoxes = this.parentElement.querySelectorAll(".letterbox");
  let allColored = true;
  for (let box of letterBoxes) {
    const color = window.getComputedStyle(box).backgroundColor;
    if (color === "rgb(51, 51, 51)") {
      allColored = false;
      break;
    }
  }
  const processButton = this.parentElement.querySelector("button");
  processButton.disabled = !allColored;
}

function processGuess() {
  const letterBoxes = this.parentElement.querySelectorAll(".letterbox"); // Get from the *current* guess
  let guessString = "";
  letterBoxes.forEach((box) => {
    guessString += box.textContent;
  });
  console.log("Guessed word:", guessString);

  const colorMap = {
    "rgb(51, 51, 51)": "grey",
    "rgb(128, 128, 128)": "grey",
    "rgb(255, 255, 0)": "yellow",
    "rgb(0, 128, 0)": "green",
  };

  const results = [];
  letterBoxes.forEach((box) => {
    const color = window.getComputedStyle(box).backgroundColor;
    results.push(colorMap[color]);
  });

  console.log("Results:", results);

  for (let i = 0; i < guessString.length; i++) {
    const letter = guessString[i];
    if (results[i] === "green") {
      cheater.require_letter_at_position(letter, i);
      cheater.print_status();
    } else if (results[i] === "yellow") {
      cheater.require_letter(letter);
      cheater.rule_out_letter_at_position(letter, i);
      cheater.print_status();
    } else if (results[i] === "grey") {
      cheater.rule_out_letter(letter);
      cheater.print_status();
    }
  }

  wordList = cheater.clean_words;
  updateOptions();

  printAndProcessGuess(); // Print the next guess
}
