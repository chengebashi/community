window.onload = function() {
    var input = document.getElementById("upgteimg");
    var showui = document.getElementById("showui");
    var result;
    var dataArr = []; // 储存所选图片的结果(文件名和base64数据)
    var fd; //FormData方式发送请求
    var oSelect = document.getElementById("select");
    var oAdd = document.getElementById("add");
    var showinput = document.getElementById("showinput");
    var oSubmit = document.getElementById("submit");
    var oInput = document.getElementById("upgteimg");
    var lilength = showui.getElementsByTagName('li');

    function show() {
    }

    //监听展示图片的ul,执行判断是否隐藏
    showui.addEventListener("click", function () {
        show();
    });
    if (typeof FileReader === 'undefined') {
        alert("抱歉，你的浏览器不支持 FileReader");
        input.setAttribute('disabled', 'disabled');
    } else {
        input.addEventListener('change', readFile, false);
    }

    function readFile() {
        fd = new FormData();
        var iLen = this.files.length;
        var index = 0;
        var currentReViewImgIndex = 0;
        for (var i = 0; i < iLen; i++) {
            if (!input['value'].match(/.jpg|.gif|.png|.jpeg|.bmp/i)) {　　 //判断上传文件格式
                return alert("上传的图片格式不正确，请重新选择");
            }
            var reader = new FileReader();
            reader.index = i;
            fd.append(i, this.files[i]);
            reader.readAsDataURL(this.files[i]); //转成base64
            reader.fileName = this.files[i].name;
            reader.onload = function (e) {
                var imgMsg = {
                    name: this.fileName, //获取文件名
                    base64: this.result //reader.readAsDataURL方法执行完后，base64数据储存在reader.result里
                }
                dataArr.push(imgMsg);
                for (var j = 0; j < dataArr.length; j++) {
                    currentReViewImgIndex = j
                }
                result = '<div style="width: 100%;" class="showdiv"><img class="left" src="../static/images/Arrow_left.svg" /><img class="center" src="../static/images/delete.svg" /><img class="right" src="../static/images/Arrow_right.svg" /></div><img id="srcimgid' + currentReViewImgIndex + '" class="showimg" src="' + this.result + '" />';

                var li = document.createElement('li');
                li.innerHTML = result;
                showui.appendChild(li);
                var left = li.getElementsByTagName('img')[0];
                var center = li.getElementsByTagName('img')[1];
                var right = li.getElementsByTagName('img')[2];
                var src = li.getElementsByTagName('img')[3];
                show()

                left.onclick = function (num) {
                    return function () {
                        if (num == 0) {

                        } else {
                            var list = 0;
                            for (var j = 0; j < dataArr.length; j++) {
                                list = j
                            }
                            dataArr.splice(up, 0, dataArr[num]);
                            dataArr.splice(num + 1, 1)
                            var up = num - 1;
                            for (var j = 0; j < list + 1; j++) {
                                $("#srcimgid" + j + "").attr("src", dataArr[j].base64)
                            }
                            console.log(dataArr)
                        }
                    }
                }(currentReViewImgIndex)

                center.onclick = function (num) {
                    return function () {
                        li.remove(); // 在页面中删除该图片元素
                        dataArr.splice(num, 1)
                    }
                }(currentReViewImgIndex)

                right.onclick = function (num) {
                    return function () {

                        var list = 0;
                        for (var j = 0; j < dataArr.length; j++) {
                            list = j
                        }

                        dataArr.splice(list + 1, 0, dataArr[num]);
                        dataArr.splice(num, 1)
                        var down = num - 1;
                        var datalist = list + 1;
                        for (var j = 0; j < datalist; j++) {
                            $("#srcimgid" + j + "").attr("src", dataArr[j].base64)
                        }

                    }
                }(currentReViewImgIndex)
                index++;

            }
        }
    }

    function send() {
        for (var j = 0; j < dataArr.length; j++) {
            var inputdata;
            console.log(dataArr);
            // inputdata = '<input name="" type="text" id="" value="' + dataArr[j].base64 + '" />';
            // showinput.innerHTML += inputdata;
        }
        var community = $('#community_name').html();
        data_data = {'community':community,'image_data':dataArr};
        $.ajax({
                type:'POST',
                contentType:'application/json; charset = UTF-8',
                dataType: 'json',
                url: '/addimages',
                data: JSON.stringify(data_data),
                timeout: 1000,
                success:function (data) {
                    $('#showui').html('');
                    if (data.err==0){
                        alert('上传成功');
                        window.location.reload()
                    }
                    else{
                        alert('上传失败')
                    }
                },
                error:function () {
                    alert('系统错误!')
                }
            })
    }

    oSubmit.onclick = function () {
        if (!dataArr.length) {
            return alert('请先选择文件');
        }
        send();
    }

    $('#showui').on('DOMNodeInserted', function () {
        show();
    })
}
