const { distanceXtoLine } = require('./tools');

class Spaceship {
    constructor(arrowTheta) {
        this.Enemies = [];
        this.arrowTheta = arrowTheta;
        this.laserTheta = this.laserTheta();
    }
    laserTheta() {
        this.laserTheta = [];
        for (let k = 0; k < 8; k++) {
            this.laserTheta.push(k * Math.PI / 4);
        }
        return this.laserTheta;
    }
    lines() {
        this.lines = [];
        for (let k = 0; k < 8; k++) {
            let theta = this.laserTheta[k];
            let a = Math.cos(theta);
            let b = Math.sin(theta);
            this.lines.push([a, b]);
        }
        return this.lines;
    }
    checkOnLines() {
        this.listEnemy = [];
        for (let enemy of this.Enemies) {
            let X = enemy.coord;
            let theta = enemy.theta;
            let r = enemy.radius;
            for (let line of this.lines) {
                if (distanceXtoLine(X, line) < r) {
                    this.listEnemy.push(theta);
                }
            }
        }
        return this.listEnemy;
    }
}

module.exports = { Spaceship }