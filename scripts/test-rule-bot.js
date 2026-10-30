// Plays every possible tic-tac-toe game against the Lesson 1.4 rule bot.
//   node scripts/test-rule-bot.js
// Checks that with every rule on the bot never loses, whoever goes first and
// whichever square it picks when a rule allows more than one. Then, for each
// rule turned off alone, reports whether a student can beat the bot.
const fs = require("fs");
const path = require("path");
const src = fs.readFileSync(path.join(__dirname, "../assets/Unit_1/rule_bot.html"), "utf8");
const logic = src.slice(src.indexOf("// BEGIN LOGIC"), src.indexOf("// END LOGIC"));
const { RULES, botChoices, winner, empty } = new Function(logic + "; return { RULES, botChoices, winner, empty };")();

// Can the human force a win from here? Bot may pick any allowed square
// (the human wins only if every bot choice still loses).
function humanCanWin(b, toMove, on) {
  const w = winner(b);
  if (w) return w.who === "X";
  if (empty(b).length === 0) return false;
  if (toMove === "X") {
    return empty(b).some((i) => { const c = b.slice(); c[i] = "X"; return humanCanWin(c, "O", on); });
  }
  const { squares } = botChoices(b, "O", "X", on);
  // a student can beat the bot if SOME bot choice leads to a forced win
  return squares.some((i) => { const c = b.slice(); c[i] = "O"; return humanCanWin(c, "X", on); });
}
function botNeverLoses(on) {
  const start = Array(9).fill(null);
  return !humanCanWin(start, "X", on) && !humanCanWin(start, "O", on);
}

const all = RULES.map(() => true);
let ok = true;
if (!botNeverLoses(all)) { console.log("FAIL: the bot can lose with every rule on"); ok = false; }
else console.log("ok: with every rule on, the bot never loses (both starts, every choice)");
RULES.forEach((r, k) => {
  const on = RULES.map((_, i) => i !== k);
  console.log(`  rule ${k + 1} (${r.name}) off: ${botNeverLoses(on) ? "still unbeatable" : "beatable"}`);
});
process.exit(ok ? 0 : 1);
