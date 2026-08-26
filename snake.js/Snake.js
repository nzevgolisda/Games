const { Point } = require("./Point");

class Snake {
    constructor(p) {
        this.x = p.x;
        this.y = p.y;
        this.Vx = 1;
        this.Vy = 0;
        this.head = new Point(this.x, this.y);
        this.tail = [];
    }
}

module.exports = { Snake }