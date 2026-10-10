// Bunting math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled party-sewing norm, not a rule.
(function (root) {
"use strict";

// Labeled norms (common party-sewing references):
// - Flags: about 15 cm wide at about 5 cm gaps reads well on a string.
// - Fabric: a fat quarter is about 50 x 55 cm; two triangles nest out of each rectangle.
// - Tape: leave about 50 cm of tie at each end past the last flag.

function r1(x) { return Math.round(x * 10) / 10; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function flagCount(lengthCm, flagW, gapCm) {
  if (!positive(lengthCm)) return { error: "string length must be positive" };
  if (!positive(flagW, gapCm)) return { error: "flag width and gap must be positive" };
  var flags = Math.floor((lengthCm + gapCm) / (flagW + gapCm));
  if (flags < 1) return { error: "one flag is wider than the string" };
  var leftover = r1(lengthCm - (flags * flagW + (flags - 1) * gapCm));
  return { lengthCm: r1(lengthCm), flagW: r1(flagW), gapCm: r1(gapCm), flags: flags, leftover: leftover };
}

function renderFlags(r) {
  if (r.error) return r.error;
  return "A " + r.lengthCm + " cm string holds " + r.flags + " flags of " + r.flagW + " cm at " + r.gapCm +
    " cm gaps, with " + r.leftover + " cm of slack to share between the ends (labeled 15 cm flags, 5 cm gaps).";
}

function fabricPlan(flagW, flagH, flags) {
  if (!positive(flagW, flagH, flags)) return { error: "flag dimensions and count must be positive" };
  var across = Math.floor(50 / flagW);
  var down = Math.floor(55 / flagH);
  if (across < 1 || down < 1) return { error: "flag is bigger than a labeled fat quarter" };
  var perFQ = 2 * across * down;
  var fq = Math.ceil(flags / perFQ);
  return { flagW: r1(flagW), flagH: r1(flagH), flags: flags, perFQ: perFQ, fq: fq };
}

function renderFabric(r) {
  if (r.error) return r.error;
  return "A labeled 50 x 55 cm fat quarter nests " + r.perFQ + " flags of " + r.flagW + " x " + r.flagH +
    " cm (two per rectangle), so " + r.flags + " flags need " + r.fq + " fat quarter" + (r.fq === 1 ? "" : "s") + ".";
}

function tapePlan(lengthCm) {
  if (!positive(lengthCm)) return { error: "string length must be positive" };
  var tapeCm = r1(lengthCm + 100);
  var tapeM = r1(tapeCm / 100);
  return { lengthCm: r1(lengthCm), tapeCm: tapeCm, tapeM: tapeM };
}

function renderTape(r) {
  if (r.error) return r.error;
  return "A " + r.lengthCm + " cm span wants " + r.tapeCm + " cm of tape (" + r.tapeM +
    " m) - the flags plus a labeled 50 cm tie at each end.";
}

var api = {
  flagCount: flagCount,
  fabricPlan: fabricPlan,
  tapePlan: tapePlan,
  renderFlags: renderFlags,
  renderFabric: renderFabric,
  renderTape: renderTape
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.BuntingMath = api;
})(typeof window !== "undefined" ? window : globalThis);
