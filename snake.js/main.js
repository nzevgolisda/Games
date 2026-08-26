const { Snake } = require ('./Snake');
const { Food } = require ('./Food');
const { Point } = require ('./Point');

let p = [];
for (let i = 0; i < 4; i++) {
    p.push(new Point(i, 0));
}
let head = new Point(4, 0);
let snake = new Snake(head);
let food = new Food(new Point(5, 0));

for (let pk of p) {
    snake.tail.push(pk);
}
snake.tail.push(snake.head);
console.log(snake.tail);
// Points of Snake
let t = [];
for (let p of snake.tail) {
    let dx = snake.Vx;
    let dy = snake.Vy;
    t.push(p.move(dx, dy));
}
snake.tail = t;
console.log(snake.tail);
// Move Snake parts
let n = snake.tail.length;
if (snake.tail[n-1].isEqual(food.coord)){
    let dx = snake.Vx;
    let dy = snake.Vy;
    let pj = food.coord.move(dx, dy);
    snake.tail.push(pj);
}
console.log(snake.tail);
// Eat food
