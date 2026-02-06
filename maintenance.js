"use strict";

class Game {
  constructor() {
    this.cells = Array.from(document.querySelectorAll(".field-cell"));
    this.scoreElem = document.querySelector(".game-score");
    this.button = document.querySelector(".button.start");
    this.msgStart = document.querySelector(".message-start");
    this.msgLose = document.querySelector(".message-lose");
    this.msgWin = document.querySelector(".message-win");

    this.score = 0;
    this.field = [
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ];

    this.button.addEventListener("click", () => this.start());
    window.addEventListener("keydown", (e) => this.input(e));
  }

  start() {
    this.score = 0;
    this.field = [
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ];
    this.msgLose.classList.add("hidden");
    this.msgWin.classList.add("hidden");
    this.msgStart.classList.remove("hidden");
    this.addTile();
    this.addTile();
    this.draw();
  }

  addTile() {
    const empty = [];
    for (let r = 0; r < 4; r++)
      for (let c = 0; c < 4; c++)
        if (this.field[r][c] === 0) empty.push({ r, c });
    if (!empty.length) return;
    const { r, c } = empty[Math.floor(Math.random() * empty.length)];
    this.field[r][c] = Math.random() < 0.9 ? 2 : 4;
  }

  draw() {
    const flat = this.field.flat();
    this.cells.forEach((c, i) => {
      const v = flat[i];
      c.textContent = v || "";
      c.className = "field-cell" + (v ? ` field-cell--${v}` : "");
    });
    this.scoreElem.textContent = this.score;
  }

  input(e) {
    const old = JSON.stringify(this.field);
    if (e.key === "ArrowLeft") this.moveL();
    if (e.key === "ArrowRight") this.moveR();
    if (e.key === "ArrowUp") this.moveU();
    if (e.key === "ArrowDown") this.moveD();

    if (old !== JSON.stringify(this.field)) {
      this.addTile();
      this.draw();
      if (this.field.flat().includes(2048))
        this.msgWin.classList.remove("hidden");
      if (!this.field.flat().includes(0))
        this.msgLose.classList.remove("hidden");
    }
  }

  slide(row) {
    let f = row.filter((x) => x);
    for (let i = 0; i < f.length - 1; i++)
      if (f[i] === f[i + 1]) {
        f[i] *= 2;
        this.score += f[i];
        f[i + 1] = 0;
      }
    f = f.filter((x) => x);
    while (f.length < 4) f.push(0);
    return f;
  }

  moveL() {
    this.field = this.field.map((r) => this.slide(r));
  }
  moveR() {
    this.field = this.field.map((r) => this.slide([...r].reverse()).reverse());
  }
  moveU() {
    for (let c = 0; c < 4; c++) {
      let col = [
        this.field[0][c],
        this.field[1][c],
        this.field[2][c],
        this.field[3][c],
      ];
      col = this.slide(col);
      for (let r = 0; r < 4; r++) this.field[r][c] = col[r];
    }
  }
  moveD() {
    for (let c = 0; c < 4; c++) {
      let col = [
        this.field[3][c],
        this.field[2][c],
        this.field[1][c],
        this.field[0][c],
      ];
      col = this.slide(col);
      for (let r = 0; r < 4; r++) this.field[3 - r][c] = col[r];
    }
  }
}
new Game();
