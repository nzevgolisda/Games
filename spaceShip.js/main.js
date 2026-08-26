const { Spaceship } = require ('./Spaceship');
const { Enemy } = require ('./Enemy');
const { points } = require ('./tools');


//Objects
let spaceShip = new Spaceship(Math.PI);
// Init Enemies (dt = 0)
let dt = 0;
let n = 1;
let point = points(n);
for (let i = 0; i < n; i++) {
    let enemy = new Enemy(point[i]);
    spaceShip.Enemies.push(enemy);
    enemy.printState(dt);
}
console.log(spaceShip.lines());
console.log(spaceShip.Enemies);
console.log(spaceShip.checkOnLines());