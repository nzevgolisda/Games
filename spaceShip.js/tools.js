function getRandom(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min);
}

function getRandomFloat(min, max) {
    return Math.random() * (max - min) + min;
}

function distance(L, M) {
    let sum = 0;
    P = perp(L);
    for (let i = 0; i < 2; i++) {
        sum += (L[i] - M[i]) ** 2;
    }
    return Math.sqrt(sum);
}

function points(n) {
    let points = [];
    for (let i = 0; i < n; i++) {
        let j = getRandom(0, 2);
        let b = getRandom(0, 2);
        let bool = [true, false][b];
        let xRange = [-50, 50];
        let yRange = [-50, 50];
        if (bool === true) {
            let x = xRange[j];
            let y = getRandomFloat(-50, 50);
            bool = false;
            points.push([x, y]);
        } else if (bool === false) {
            let x = getRandomFloat(-50, 50);
            let y = yRange[j];
            bool = true;
            points.push([x, y]);
        }
    }
    return points;
}

function line(L) {
    let a = L[0];
    let b = L[1];
    return [a, b];
}

function perp(L) {
    let a = L[0];
    let b = L[1];
    return [-b, a]; // perpendicular counterclockwise to L
}

function distanceXtoLine(X, L) {
    let sum = 0;
    P = perp(L);
    for (let i = 0; i < 2; i++) {
        sum += X[i] * P[i];
    }
    return Math.abs(sum);
}

module.exports = {
    getRandom,
    points,
    distanceXtoLine,
}