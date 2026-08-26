class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
    isEqual(other) {
        if (this.x === other.x && this.y === other.y) {
            return true;
        }else {
            return false;
        }
    }
    move(dx, dy) {
        let a = this.x + dx;
        let b = this.y + dy;
        return new Point(a, b);
    }
}

module.exports = { Point }