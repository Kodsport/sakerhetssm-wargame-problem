function styleText(option, text) {
  switch (option) {
    case "underline":
      return underline(text);
    case "overline":
      return overline(text);
    case "middleline":
      return middleline(text);
    case "rainbow":
      return rainbow(text);
    case "fontsize":
      return fontsize(text);
    case "overundermiddle":
      return overundermiddle(text);
  }
  return text;
}

function underline(text) {
  return "<span style='text-decoration: underline;'>" + text + "</span>";
}
function overline(text) {
  return "<span style='text-decoration: overline;'>" + text + "</span>";
}
function middleline(text) {
  return "<span style='text-decoration: line-through;'>" + text + "</span>";
}
function rainbow(text) {
  colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"];

  let words = text.split(" ");
  let result = "";
  for (let i = 0; i < words.length; i++) {
    let word = words[i];
    let color = colors[i % colors.length];
    result += "<span style='color:" + color + "'>" + word + "</span> ";
  }
  return result;
}

function fontsize(text) {
  let result = "";
  for (let i = 0; i < text.length; i++) {
    let char = text[i];
    let size = 15 + (i % 15);
    result += "<span style='font-size: " + size + "px'>" + char + "</span>";
  }
  return result;
}

function overundermiddle(text) {
  funcs = [underline, overline, middleline];
  let words = text.split(" ");
  let result = "";
  for (let i = 0; i < words.length; i++) {
    let word = words[i];
    let func = funcs[i % funcs.length];
    result += func(word) + " ";
  }
  return result;
}
