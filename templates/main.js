const resultA = Math.round($('li').eq(0).children('.result').text() * 3.6);  //各パーセントに3.6を乗算後、四捨五入
const resultB = Math.round($('li').eq(1).children('.result').text() * 3.6);
const resultC = Math.round($('li').eq(2).children('.result').text() * 3.6);
const resultD = Math.round($('li').eq(3).children('.result').text() * 3.6);
const resultE = Math.round($('li').eq(4).children('.result').text() * 3.6);
const resultF = Math.round($('li').eq(5).children('.result').text() * 3.6);

const resultAB = resultA + 'deg ' + ( resultA + resultB ) + 'deg';  //余白に注意
const resultBC = resultA + resultB + 'deg ' + ( resultA + resultB + resultC ) + 'deg';
const resultCD = resultA + resultB + resultC + 'deg ' + ( resultA + resultB + resultC + resultD ) + 'deg';
const resultDE = resultA + resultB + resultC + resultD + 'deg ' + ( resultA + resultB + resultC + resultD + resultE )  + 'deg';
const resultEF = resultA + resultB + resultC + resultD + resultE + 'deg ' + '360deg'; //最後の数値は360度に揃える

$('#circle').css('background', 'conic-gradient(#dbcdf0 ' + resultA + 'deg, #c9e4de ' + resultAB + ', #faedcb ' + resultBC + ', #c6def1 ' + resultCD + ', #f2c6de ' + resultDE + ', #f7d9c4 ' + resultEF + ')');