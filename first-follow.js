const firstFollow = require('first-follow');

const rules = [
  // S -> a b A
  {
    left: 'S',
    right: ['a', 'b', 'A']
  },

  // A -> b c
  {
    left: 'A',
    right: ['b', 'c']
  },

  // A -> ε
  {
    left: 'A',
    right: [null]
  }
];

const { firstSets, followSets, predictSets } = firstFollow(rules);

console.log(firstSets);
/*
 *  // S: a
 *  // A: b, ε
 *
 *  {
 *    S: ['a'],
 *    A: ['b', null]
 *  }
 */


console.log(followSets);
/*
 *  // S: ┤
 *  // A: ┤
 *
 *  {
 *    S: ['\u0000'],
 *    A: ['\u0000']
 *  }
 */

console.log(predictSets);
/*
 *  // 1: a
 *  // 2: b
 *  // 3: ┤
 *
 *  {
 *    '1': ['a'],
 *    '2': ['b'],
 *    '3': ['\u0000']
 *  }
*/