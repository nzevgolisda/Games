class Enemy {
    constructor(coord) {
        this.radius = 1;
        this.coord = coord;
        this.theta = Math.atan(this.coord[1] / this.coord[0]);
    }
    velocity(dt) {
        this.Vo = 1;
        if (dt === 0) {
            this.Vx = this.Vo * Math.cos(this.theta);
            this.Vy = this.Vo * Math.sin(this.theta);
            this.velocity = [this.Vx, this.Vy];
            return this.velocity;
        } else if (dt > 0) {
            this.Vx = this.Vo * Math.cos(this.theta);
            this.Vy = this.Vo * Math.sin(this.theta);
            this.moveEnemy(dt);
            this.velocity = [this.Vx, this.Vy];
            return this.velocity;
        }
    }
    moveEnemy(dt) {
        this.x += this.Vx * dt;
        this.y += this.Vy * dt;
    }
    printState(dt = 0) {
        console.log(this.coord);
        console.log(this.velocity(dt));
        console.log(this.theta / Math.PI + 'pi');
        console.log('# dt = ' + dt);
    }
}

module.exports = { Enemy }
