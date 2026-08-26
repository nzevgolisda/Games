const { Point } = require("./Point");

class Food {
    constructor(p) {
        this.x = p.x;
        this.y = p.y;
        this.radius = 1;
        this.coord = new Point(this.x, this.y);
    }
}

module.exports = { Food }