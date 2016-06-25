
var huffman = require("n-ary-huffman")
var elements = [{name:'Alanine', weight:7.4}, 
            {name:'Arginine', weight:4.2}, 
            {name:'Asparagine', weight:4.4}, 
            {name:'Aspartic Acid', weight:5.9}, 
            {name:'Cystine', weight:3.3}, 
            {name:'Glutamic Acid', weight:5.8},
            {name:'Glutamine', weight:3.7}, 
            {name:'Glycine', weight:7.4}, 
            {name:'Histidine', weight:2.9}, 
            {name:'Isoleucine', weight:3.8}, 
            {name:'Leucine', weight:7.5}, 
            {name:'Lysine', weight:7.2}, 
            {name:'Methionine', weight:1.8}, 
            {name:'Phenylalanine', weight:4.0}, 
            {name:'Proline', weight:5.0}, 
            {name:'Serine', weight:8.0}, 
            {name:'Threonine', weight:6.2},
            {name:'Tryptophan', weight:1.3}, 
            {name:'Tyrosine', weight:3.3}, 
            {name:'Valine', weight:6.8}, 
            {name:'Stop Codons', weight:0.1}];


var alphabet = "0123"
 
var tree = huffman.createTree(elements, alphabet.length)
tree.assignCodeWords(alphabet, function(element, code) {
  console.log(element, code)
})