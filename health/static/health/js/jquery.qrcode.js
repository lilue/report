
function QR8bitByte(a){
	this.mode=QRMode.MODE_8BIT_BYTE,
	this.data=a
}

function QRCode(a,b){
	this.typeNumber=a,
	this.errorCorrectLevel=b,
	this.modules=null,
	this.moduleCount=0,
	this.dataCache=null,
	this.dataList=new Array()
}
function QRPolynomial(a,b){
	var c,d;
	if(void 0==a.length){
		throw new Error(a.length+"/"+b)
	}
	for(c=0;c<a.length&&0==a[c];){
		c++
	}
	for(this.num=new Array(a.length-c+b),d=0;d<a.length-c;d++){
		this.num[d]=a[d+c]
	}
}
function QRRSBlock(a,b){
	this.totalCount=a,
	this.dataCount=b
}
function QRBitBuffer(){
	this.buffer=new Array(),
	this.length=0
}
function utf16to8(str) {
    var out, i, len, c;

    out = "";
    len = str.length;
    for(i = 0; i < len; i++) {
	c = str.charCodeAt(i);
	if ((c >= 0x0001) && (c <= 0x007F)) {
	    out += str.charAt(i);
	} else if (c > 0x07FF) {
	    out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
	    out += String.fromCharCode(0x80 | ((c >>  6) & 0x3F));
	    out += String.fromCharCode(0x80 | ((c >>  0) & 0x3F));
	} else {
	    out += String.fromCharCode(0xC0 | ((c >>  6) & 0x1F));
	    out += String.fromCharCode(0x80 | ((c >>  0) & 0x3F));
	}
    }
    return out;
}
function utf8to16(str) {
    var out, i, len, c;
    var char2, char3;

    out = "";
    len = str.length;
    i = 0;
    while(i < len) {
	c = str.charCodeAt(i++);
	switch(c >> 4)
	{
	  case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
	    // 0xxxxxxx
	    out += str.charAt(i-1);
	    break;
	  case 12: case 13:
	    // 110x xxxx   10xx xxxx
	    char2 = str.charCodeAt(i++);
	    out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
	    break;
	  case 14:
	    // 1110 xxxx  10xx xxxx  10xx xxxx
	    char2 = str.charCodeAt(i++);
	    char3 = str.charCodeAt(i++);
	    out += String.fromCharCode(((c & 0x0F) << 12) |
					   ((char2 & 0x3F) << 6) |
					   ((char3 & 0x3F) << 0));
	    break;
	}
    }

    return out;
}
var QRMode,QRErrorCorrectLevel,QRMaskPattern,QRUtil,QRMath,i;
for(function(a){
	a.fn.qrcode=function(b){
		var c,d;
		return"string"==typeof b&&(b={text:b}),
		b=a.extend({},{
			render:"canvas",
			width:256,
			height:256,
			//这里是图片的高度和宽度
			imgWidth:b.width/5,
			imgHeight:b.height/5,
			typeNumber:-1,
			correctLevel:QRErrorCorrectLevel.H,
			background:"#ffffff",
			foreground:"#000000"
		 },b),c=function(){
			var c,d,e,f,g,h,i,j,k,a=new QRCode(b.typeNumber,b.correctLevel);
			for(a.addData(utf16to8(b.text)),a.make(),
					c=document.createElement("canvas"),
					c.width=b.width,c.height=b.height,d=c.getContext("2d"),
					b.src&&(e=new Image(),e.src=b.src,e.onload=function(){
						d.drawImage(e,(b.width-b.imgWidth)/2,(b.height-b.imgHeight)/2,
								b.imgWidth,b.imgHeight)}),f=b.width/a.getModuleCount(),
								g=b.height/a.getModuleCount(),h=0;h<a.getModuleCount();h++)
			{for(i=0;i<a.getModuleCount();i++){
				d.fillStyle=a.isDark(h,i)?b.foreground:b.background,
						j=Math.ceil((i+1)*f)-Math.floor(i*f),
						k=Math.ceil((h+1)*f)-Math.floor(h*f),
						d.fillRect(Math.round(i*f),Math.round(h*g),j,k)
						}}return c},
						d=function(){var d,e,f,g,h,i,
							c=new QRCode(b.typeNumber,b.correctLevel);
						//这里的utf16to8(b.text)是对Text中的字符串进行转码，让其支持中文
						for(c.addData(utf16to8(b.text)),c.make(),d=a("<table></table>").css("width",b.width+"px").css("height",b.height+"px").css("border","0px").css("border-collapse","collapse").css("background-color",b.background),e=b.width/c.getModuleCount(),f=b.height/c.getModuleCount(),g=0;g<c.getModuleCount();g++){for(h=a("<tr></tr>").css("height",f+"px").appendTo(d),i=0;i<c.getModuleCount();i++){a("<td></td>").css("width",e+"px").css("background-color",c.isDark(g,i)?b.foreground:b.background).appendTo(h)}}return d},this.each(function(){var e="canvas"==b.render?c():d();a(e).appendTo(this)})}}(jQuery),QR8bitByte.prototype={getLength:function(){return this.data.length},write:function(a){for(var b=0;b<this.data.length;b++){a.put(this.data.charCodeAt(b),8)}}},QRCode.prototype={addData:function(a){var b=new QR8bitByte(a);this.dataList.push(b),this.dataCache=null},isDark:function(a,b){if(0>a||this.moduleCount<=a||0>b||this.moduleCount<=b){throw new Error(a+","+b)}return this.modules[a][b]},getModuleCount:function(){return this.moduleCount},make:function(){var a,b,c,d,e,f;if(this.typeNumber<1){for(a=1,a=1;40>a;a++){for(b=QRRSBlock.getRSBlocks(a,this.errorCorrectLevel),c=new QRBitBuffer(),d=0,e=0;e<b.length;e++){d+=b[e].dataCount}for(e=0;e<this.dataList.length;e++){f=this.dataList[e],c.put(f.mode,4),c.put(f.getLength(),QRUtil.getLengthInBits(f.mode,a)),f.write(c)}if(c.getLengthInBits()<=8*d){break}}this.typeNumber=a}this.makeImpl(!1,this.getBestMaskPattern())},makeImpl:function(a,b){var c,d;for(this.moduleCount=4*this.typeNumber+17,this.modules=new Array(this.moduleCount),c=0;c<this.moduleCount;c++){for(this.modules[c]=new Array(this.moduleCount),d=0;d<this.moduleCount;d++){this.modules[c][d]=null}}this.setupPositionProbePattern(0,0),this.setupPositionProbePattern(this.moduleCount-7,0),this.setupPositionProbePattern(0,this.moduleCount-7),this.setupPositionAdjustPattern(),this.setupTimingPattern(),this.setupTypeInfo(a,b),this.typeNumber>=7&&this.setupTypeNumber(a),null==this.dataCache&&(this.dataCache=QRCode.createData(this.typeNumber,this.errorCorrectLevel,this.dataList)),this.mapData(this.dataCache,b)},setupPositionProbePattern:function(a,b){var c,d;for(c=-1;7>=c;c++){if(!(-1>=a+c||this.moduleCount<=a+c)){for(d=-1;7>=d;d++){-1>=b+d||this.moduleCount<=b+d||(this.modules[a+c][b+d]=c>=0&&6>=c&&(0==d||6==d)||d>=0&&6>=d&&(0==c||6==c)||c>=2&&4>=c&&d>=2&&4>=d?!0:!1)}}}},getBestMaskPattern:function(){var c,d,a=0,b=0;for(c=0;8>c;c++){this.makeImpl(!0,c),d=QRUtil.getLostPoint(this),(0==c||a>d)&&(a=d,b=c)}return b},createMovieClip:function(a,b,c){var f,g,h,i,j,d=a.createEmptyMovieClip(b,c),e=1;for(this.make(),f=0;f<this.modules.length;f++){for(g=f*e,h=0;h<this.modules[f].length;h++){i=h*e,j=this.modules[f][h],j&&(d.beginFill(0,100),d.moveTo(i,g),d.lineTo(i+e,g),d.lineTo(i+e,g+e),d.lineTo(i,g+e),d.endFill())}}return d},setupTimingPattern:function(){var a,b;for(a=8;a<this.moduleCount-8;a++){null==this.modules[a][6]&&(this.modules[a][6]=0==a%2)}for(b=8;b<this.moduleCount-8;b++){null==this.modules[6][b]&&(this.modules[6][b]=0==b%2)}},setupPositionAdjustPattern:function(){var b,c,d,e,f,g,a=QRUtil.getPatternPosition(this.typeNumber);for(b=0;b<a.length;b++){for(c=0;c<a.length;c++){if(d=a[b],e=a[c],null==this.modules[d][e]){for(f=-2;2>=f;f++){for(g=-2;2>=g;g++){this.modules[d+f][e+g]=-2==f||2==f||-2==g||2==g||0==f&&0==g?!0:!1}}}}}},setupTypeNumber:function(a){var c,d,b=QRUtil.getBCHTypeNumber(this.typeNumber);for(c=0;18>c;c++){d=!a&&1==(1&b>>c),this.modules[Math.floor(c/3)][c%3+this.moduleCount-8-3]=d}for(c=0;18>c;c++){d=!a&&1==(1&b>>c),this.modules[c%3+this.moduleCount-8-3][Math.floor(c/3)]=d}},setupTypeInfo:function(a,b){var e,f,c=this.errorCorrectLevel<<3|b,d=QRUtil.getBCHTypeInfo(c);for(e=0;15>e;e++){f=!a&&1==(1&d>>e),6>e?this.modules[e][8]=f:8>e?this.modules[e+1][8]=f:this.modules[this.moduleCount-15+e][8]=f}for(e=0;15>e;e++){f=!a&&1==(1&d>>e),8>e?this.modules[8][this.moduleCount-e-1]=f:9>e?this.modules[8][15-e-1+1]=f:this.modules[8][15-e-1]=f}this.modules[this.moduleCount-8][8]=!a},mapData:function(a,b){var g,h,i,j,c=-1,d=this.moduleCount-1,e=7,f=0;for(g=this.moduleCount-1;g>0;g-=2){for(6==g&&g--;;){for(h=0;2>h;h++){null==this.modules[d][g-h]&&(i=!1,f<a.length&&(i=1==(1&a[f]>>>e)),j=QRUtil.getMask(b,d,g-h),j&&(i=!i),this.modules[d][g-h]=i,e--,-1==e&&(f++,e=7))}if(d+=c,0>d||this.moduleCount<=d){d-=c,c=-c;break}}}}},QRCode.PAD0=236,QRCode.PAD1=17,QRCode.createData=function(a,b,c){var f,g,h,d=QRRSBlock.getRSBlocks(a,b),e=new QRBitBuffer();for(f=0;f<c.length;f++){g=c[f],e.put(g.mode,4),e.put(g.getLength(),QRUtil.getLengthInBits(g.mode,a)),g.write(e)}for(h=0,f=0;f<d.length;f++){h+=d[f].dataCount}if(e.getLengthInBits()>8*h){throw new Error("code length overflow. ("+e.getLengthInBits()+">"+8*h+")")}for(e.getLengthInBits()+4<=8*h&&e.put(0,4);0!=e.getLengthInBits()%8;){e.putBit(!1)}for(;;){if(e.getLengthInBits()>=8*h){break}if(e.put(QRCode.PAD0,8),e.getLengthInBits()>=8*h){break}e.put(QRCode.PAD1,8)}return QRCode.createBytes(e,d)},QRCode.createBytes=function(a,b){var h,i,j,k,l,m,n,o,p,q,r,c=0,d=0,e=0,f=new Array(b.length),g=new Array(b.length);for(h=0;h<b.length;h++){for(i=b[h].dataCount,j=b[h].totalCount-i,d=Math.max(d,i),e=Math.max(e,j),f[h]=new Array(i),k=0;k<f[h].length;k++){f[h][k]=255&a.buffer[k+c]}for(c+=i,l=QRUtil.getErrorCorrectPolynomial(j),m=new QRPolynomial(f[h],l.getLength()-1),n=m.mod(l),g[h]=new Array(l.getLength()-1),k=0;k<g[h].length;k++){o=k+n.getLength()-g[h].length,g[h][k]=o>=0?n.get(o):0}}for(p=0,k=0;k<b.length;k++){p+=b[k].totalCount}for(q=new Array(p),r=0,k=0;d>k;k++){for(h=0;h<b.length;h++){k<f[h].length&&(q[r++]=f[h][k])}}for(k=0;e>k;k++){for(h=0;h<b.length;h++){k<g[h].length&&(q[r++]=g[h][k])}}return q},QRMode={MODE_NUMBER:1,MODE_ALPHA_NUM:2,MODE_8BIT_BYTE:4,MODE_KANJI:8},QRErrorCorrectLevel={L:1,M:0,Q:3,H:2},QRMaskPattern={PATTERN000:0,PATTERN001:1,PATTERN010:2,PATTERN011:3,PATTERN100:4,PATTERN101:5,PATTERN110:6,PATTERN111:7},QRUtil={PATTERN_POSITION_TABLE:[[],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46],[6,28,50],[6,30,54],[6,32,58],[6,34,62],[6,26,46,66],[6,26,48,70],[6,26,50,74],[6,30,54,78],[6,30,56,82],[6,30,58,86],[6,34,62,90],[6,28,50,72,94],[6,26,50,74,98],[6,30,54,78,102],[6,28,54,80,106],[6,32,58,84,110],[6,30,58,86,114],[6,34,62,90,118],[6,26,50,74,98,122],[6,30,54,78,102,126],[6,26,52,78,104,130],[6,30,56,82,108,134],[6,34,60,86,112,138],[6,30,58,86,114,142],[6,34,62,90,118,146],[6,30,54,78,102,126,150],[6,24,50,76,102,128,154],[6,28,54,80,106,132,158],[6,32,58,84,110,136,162],[6,26,54,82,110,138,166],[6,30,58,86,114,142,170]],G15:1335,G18:7973,G15_MASK:21522,getBCHTypeInfo:function(a){for(var b=a<<10;QRUtil.getBCHDigit(b)-QRUtil.getBCHDigit(QRUtil.G15)>=0;){b^=QRUtil.G15<<QRUtil.getBCHDigit(b)-QRUtil.getBCHDigit(QRUtil.G15)}return(a<<10|b)^QRUtil.G15_MASK},getBCHTypeNumber:function(a){for(var b=a<<12;QRUtil.getBCHDigit(b)-QRUtil.getBCHDigit(QRUtil.G18)>=0;){b^=QRUtil.G18<<QRUtil.getBCHDigit(b)-QRUtil.getBCHDigit(QRUtil.G18)}return a<<12|b},getBCHDigit:function(a){for(var b=0;0!=a;){b++,a>>>=1}return b},getPatternPosition:function(a){return QRUtil.PATTERN_POSITION_TABLE[a-1]},getMask:function(a,b,c){switch(a){case QRMaskPattern.PATTERN000:return 0==(b+c)%2;case QRMaskPattern.PATTERN001:return 0==b%2;case QRMaskPattern.PATTERN010:return 0==c%3;case QRMaskPattern.PATTERN011:return 0==(b+c)%3;case QRMaskPattern.PATTERN100:return 0==(Math.floor(b/2)+Math.floor(c/3))%2;case QRMaskPattern.PATTERN101:return 0==b*c%2+b*c%3;case QRMaskPattern.PATTERN110:return 0==(b*c%2+b*c%3)%2;case QRMaskPattern.PATTERN111:return 0==(b*c%3+(b+c)%2)%2;default:throw new Error("bad maskPattern:"+a)}},getErrorCorrectPolynomial:function(a){var c,b=new QRPolynomial([1],0);for(c=0;a>c;c++){b=b.multiply(new QRPolynomial([1,QRMath.gexp(c)],0))}return b},getLengthInBits:function(a,b){if(b>=1&&10>b){switch(a){case QRMode.MODE_NUMBER:return 10;case QRMode.MODE_ALPHA_NUM:return 9;case QRMode.MODE_8BIT_BYTE:return 8;case QRMode.MODE_KANJI:return 8;default:throw new Error("mode:"+a)}}else{if(27>b){switch(a){case QRMode.MODE_NUMBER:return 12;case QRMode.MODE_ALPHA_NUM:return 11;case QRMode.MODE_8BIT_BYTE:return 16;case QRMode.MODE_KANJI:return 10;default:throw new Error("mode:"+a)}}else{if(!(41>b)){throw new Error("type:"+b)}switch(a){case QRMode.MODE_NUMBER:return 14;case QRMode.MODE_ALPHA_NUM:return 13;case QRMode.MODE_8BIT_BYTE:return 16;case QRMode.MODE_KANJI:return 12;default:throw new Error("mode:"+a)}}}},getLostPoint:function(a){var d,e,f,g,h,i,j,k,l,b=a.getModuleCount(),c=0;for(d=0;b>d;d++){for(e=0;b>e;e++){for(f=0,g=a.isDark(d,e),h=-1;1>=h;h++){if(!(0>d+h||d+h>=b)){for(i=-1;1>=i;i++){0>e+i||e+i>=b||(0!=h||0!=i)&&g==a.isDark(d+h,e+i)&&f++}}}f>5&&(c+=3+f-5)}}for(d=0;b-1>d;d++){for(e=0;b-1>e;e++){j=0,a.isDark(d,e)&&j++,a.isDark(d+1,e)&&j++,a.isDark(d,e+1)&&j++,a.isDark(d+1,e+1)&&j++,(0==j||4==j)&&(c+=3)}}for(d=0;b>d;d++){for(e=0;b-6>e;e++){a.isDark(d,e)&&!a.isDark(d,e+1)&&a.isDark(d,e+2)&&a.isDark(d,e+3)&&a.isDark(d,e+4)&&!a.isDark(d,e+5)&&a.isDark(d,e+6)&&(c+=40)}}for(e=0;b>e;e++){for(d=0;b-6>d;d++){a.isDark(d,e)&&!a.isDark(d+1,e)&&a.isDark(d+2,e)&&a.isDark(d+3,e)&&a.isDark(d+4,e)&&!a.isDark(d+5,e)&&a.isDark(d+6,e)&&(c+=40)}}for(k=0,e=0;b>e;e++){for(d=0;b>d;d++){a.isDark(d,e)&&k++}}return l=Math.abs(100*k/b/b-50)/5,c+=10*l}},QRMath={glog:function(a){if(1>a){throw new Error("glog("+a+")")}return QRMath.LOG_TABLE[a]},gexp:function(a){for(;0>a;){a+=255}for(;a>=256;){a-=255}return QRMath.EXP_TABLE[a]},EXP_TABLE:new Array(256),LOG_TABLE:new Array(256)},i=0;8>i;i++){QRMath.EXP_TABLE[i]=1<<i}for(i=8;256>i;i++){QRMath.EXP_TABLE[i]=QRMath.EXP_TABLE[i-4]^QRMath.EXP_TABLE[i-5]^QRMath.EXP_TABLE[i-6]^QRMath.EXP_TABLE[i-8]}for(i=0;255>i;i++){QRMath.LOG_TABLE[QRMath.EXP_TABLE[i]]=i}QRPolynomial.prototype={get:function(a){return this.num[a]},getLength:function(){return this.num.length},multiply:function(a){var c,d,b=new Array(this.getLength()+a.getLength()-1);for(c=0;c<this.getLength();c++){for(d=0;d<a.getLength();d++){b[c+d]^=QRMath.gexp(QRMath.glog(this.get(c))+QRMath.glog(a.get(d)))}}return new QRPolynomial(b,0)},mod:function(a){var b,c,d;if(this.getLength()-a.getLength()<0){return this}for(b=QRMath.glog(this.get(0))-QRMath.glog(a.get(0)),c=new Array(this.getLength()),d=0;d<this.getLength();d++){c[d]=this.get(d)}for(d=0;d<a.getLength();d++){c[d]^=QRMath.gexp(QRMath.glog(a.get(d))+b)}return new QRPolynomial(c,0).mod(a)}},QRRSBlock.RS_BLOCK_TABLE=[[1,26,19],[1,26,16],[1,26,13],[1,26,9],[1,44,34],[1,44,28],[1,44,22],[1,44,16],[1,70,55],[1,70,44],[2,35,17],[2,35,13],[1,100,80],[2,50,32],[2,50,24],[4,25,9],[1,134,108],[2,67,43],[2,33,15,2,34,16],[2,33,11,2,34,12],[2,86,68],[4,43,27],[4,43,19],[4,43,15],[2,98,78],[4,49,31],[2,32,14,4,33,15],[4,39,13,1,40,14],[2,121,97],[2,60,38,2,61,39],[4,40,18,2,41,19],[4,40,14,2,41,15],[2,146,116],[3,58,36,2,59,37],[4,36,16,4,37,17],[4,36,12,4,37,13],[2,86,68,2,87,69],[4,69,43,1,70,44],[6,43,19,2,44,20],[6,43,15,2,44,16],[4,101,81],[1,80,50,4,81,51],[4,50,22,4,51,23],[3,36,12,8,37,13],[2,116,92,2,117,93],[6,58,36,2,59,37],[4,46,20,6,47,21],[7,42,14,4,43,15],[4,133,107],[8,59,37,1,60,38],[8,44,20,4,45,21],[12,33,11,4,34,12],[3,145,115,1,146,116],[4,64,40,5,65,41],[11,36,16,5,37,17],[11,36,12,5,37,13],[5,109,87,1,110,88],[5,65,41,5,66,42],[5,54,24,7,55,25],[11,36,12],[5,122,98,1,123,99],[7,73,45,3,74,46],[15,43,19,2,44,20],[3,45,15,13,46,16],[1,135,107,5,136,108],[10,74,46,1,75,47],[1,50,22,15,51,23],[2,42,14,17,43,15],[5,150,120,1,151,121],[9,69,43,4,70,44],[17,50,22,1,51,23],[2,42,14,19,43,15],[3,141,113,4,142,114],[3,70,44,11,71,45],[17,47,21,4,48,22],[9,39,13,16,40,14],[3,135,107,5,136,108],[3,67,41,13,68,42],[15,54,24,5,55,25],[15,43,15,10,44,16],[4,144,116,4,145,117],[17,68,42],[17,50,22,6,51,23],[19,46,16,6,47,17],[2,139,111,7,140,112],[17,74,46],[7,54,24,16,55,25],[34,37,13],[4,151,121,5,152,122],[4,75,47,14,76,48],[11,54,24,14,55,25],[16,45,15,14,46,16],[6,147,117,4,148,118],[6,73,45,14,74,46],[11,54,24,16,55,25],[30,46,16,2,47,17],[8,132,106,4,133,107],[8,75,47,13,76,48],[7,54,24,22,55,25],[22,45,15,13,46,16],[10,142,114,2,143,115],[19,74,46,4,75,47],[28,50,22,6,51,23],[33,46,16,4,47,17],[8,152,122,4,153,123],[22,73,45,3,74,46],[8,53,23,26,54,24],[12,45,15,28,46,16],[3,147,117,10,148,118],[3,73,45,23,74,46],[4,54,24,31,55,25],[11,45,15,31,46,16],[7,146,116,7,147,117],[21,73,45,7,74,46],[1,53,23,37,54,24],[19,45,15,26,46,16],[5,145,115,10,146,116],[19,75,47,10,76,48],[15,54,24,25,55,25],[23,45,15,25,46,16],[13,145,115,3,146,116],[2,74,46,29,75,47],[42,54,24,1,55,25],[23,45,15,28,46,16],[17,145,115],[10,74,46,23,75,47],[10,54,24,35,55,25],[19,45,15,35,46,16],[17,145,115,1,146,116],[14,74,46,21,75,47],[29,54,24,19,55,25],[11,45,15,46,46,16],[13,145,115,6,146,116],[14,74,46,23,75,47],[44,54,24,7,55,25],[59,46,16,1,47,17],[12,151,121,7,152,122],[12,75,47,26,76,48],[39,54,24,14,55,25],[22,45,15,41,46,16],[6,151,121,14,152,122],[6,75,47,34,76,48],[46,54,24,10,55,25],[2,45,15,64,46,16],[17,152,122,4,153,123],[29,74,46,14,75,47],[49,54,24,10,55,25],[24,45,15,46,46,16],[4,152,122,18,153,123],[13,74,46,32,75,47],[48,54,24,14,55,25],[42,45,15,32,46,16],[20,147,117,4,148,118],[40,75,47,7,76,48],[43,54,24,22,55,25],[10,45,15,67,46,16],[19,148,118,6,149,119],[18,75,47,31,76,48],[34,54,24,34,55,25],[20,45,15,61,46,16]],QRRSBlock.getRSBlocks=function(a,b){var d,e,f,g,h,i,j,c=QRRSBlock.getRsBlockTable(a,b);if(void 0==c){throw new Error("bad rs block @ typeNumber:"+a+"/errorCorrectLevel:"+b)}for(d=c.length/3,e=new Array(),f=0;d>f;f++){for(g=c[3*f+0],h=c[3*f+1],i=c[3*f+2],j=0;g>j;j++){e.push(new QRRSBlock(h,i))}}return e},QRRSBlock.getRsBlockTable=function(a,b){switch(b){case QRErrorCorrectLevel.L:return QRRSBlock.RS_BLOCK_TABLE[4*(a-1)+0];case QRErrorCorrectLevel.M:return QRRSBlock.RS_BLOCK_TABLE[4*(a-1)+1];case QRErrorCorrectLevel.Q:return QRRSBlock.RS_BLOCK_TABLE[4*(a-1)+2];case QRErrorCorrectLevel.H:return QRRSBlock.RS_BLOCK_TABLE[4*(a-1)+3];default:return void 0}},QRBitBuffer.prototype={get:function(a){var b=Math.floor(a/8);return 1==(1&this.buffer[b]>>>7-a%8)},put:function(a,b){for(var c=0;b>c;c++){this.putBit(1==(1&a>>>b-c-1))}},getLengthInBits:function(){return this.length},putBit:function(a){var b=Math.floor(this.length/8);this.buffer.length<=b&&this.buffer.push(0),a&&(this.buffer[b]|=128>>>this.length%8),this.length++}};
