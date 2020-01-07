




//创建笔记点击后，显示表单
function form_note_create(obj,basedir_id,note_type) {  
    //显示文件夹为打开状态
    $(obj).parent().children(".open").removeClass("open").addClass( "close");
    $(obj).parent().children(".pack").removeClass("pack").addClass( "unpack");
    //以下代码使显示该文件夹下面的文件列表代码不再隐藏
    $(obj).parent().next().show();
    //以下代码为了网络更新文件夹下的文件列表，在手机上会增加操作
    //目前给予隐藏功能，因为用户目的是新建，不是浏览
    //$.get('/notebook/note/list/'+basedir_id,function(result){ $("#ul_"+basedir_id).html(result); });
    //显示新建表单
    $.get("/notebook/form/note/create/"+basedir_id+"/"+note_type,function(result){
                $(".main").html(result);
            });

    event.stopPropagation();

}
//显示笔记
function retrieve(obj,id) {  
    $.get("/notebook/note/retrieve/"+id,function(result){
                $(".main").html(result);
            });
    fold(obj,id);//打开折叠文件夹
}


//更新笔记表单
function form_update(id) {  
    $.get("/notebook/form/note/update/"+id,function(result){
                $(".main").html(result);
            });
}

//创建笔记
function note_create(basedir_id) {  
        $("#text1").val($(".w-e-text").html());
        $.ajax({
            type:"POST",
            url:"/notebook/note/create/",
            data:$("#form_note_create").serialize(),
            success:function(data){ 
                $("#ul_"+basedir_id).prepend(data);
                $("#scroll").html('<button type="button" class="btn btn-primary"><h4>创建成功!</h4></button>'); 
            },
        });
}

//更新笔记
function note_update(id) {  
        $("#text1").val($(".w-e-text").html());
        $.ajax({
            type:"POST",
            url:"/notebook/note/update/",
            data:$("#form_note_update").serialize(),
            success:function(data){
               $("#title_"+id).text(data); 
                $.get("/notebook/note/retrieve/"+id, function(result){
                    $(".main").html(result); 
                });

            },
        });
}

//笔记移到回收站
function note_remove(id) {
    //1秒后更新main中的数据，否则模式对话框不能正确退出
     setTimeout(
         function () { 
            $.get('/notebook/note/remove/'+id,function(result){
                $('.main').html(result);
            });//end of $.get
         }, 
         500
     );//end of setTimeout
    $('#li_'+id).remove();
}

//清空回收站
function empty_recycle_bin(id) {
    //id为回收站的id
    //1秒后更新main中的数据，否则模式对话框不能正确退出
     setTimeout(
         function () { 
            $.get('/notebook/note/empty_recycle_bin/',function(result){
                $('.main').html(result);
            });//end of $.get
         }, 
         500
     );//end of setTimeout
    $('#ul_'+id).html("");
}

//显示已删除笔记列表
function show_deleted(obj){
        $.get('/notebook/note/list/show_deleted',function(result){ $("#ul_0").html(result); });
}

//折叠文件夹
function fold(obj,id) {
    if ($(obj).next().css("display") == "none") {
        $(obj).children(".open").removeClass("open").addClass(
                "close");
        $(obj).children(".pack").removeClass("pack").addClass(
                "unpack");
        $.get('/notebook/note/list/'+id,function(result){ $("#ul_"+id).html(result); });
        $(obj).next().fadeToggle();
    } else {
        $(obj).children(".close").removeClass("close")
                .addClass("open");
        $(obj).children(".unpack").removeClass("unpack")
                .addClass("pack");
        $(obj).next().html("");
        $(obj).next().fadeToggle();
    }
}


//拖拽事件定义

function dragStart(event,obj) {
    //alert($(obj).attr('id'));
    event.dataTransfer.setData("target_id", event.target.id);
    event.target.style.opacity = "0.5";    
}
function dragEnd(event,obj) {
    event.target.style.opacity = "1";
}
function dragOver(event,obj) {
    event.preventDefault();
    event.stopPropagation();
}
function dragEnter(event,obj){
    event.stopPropagation();

    //title被拖拽效果显示在div上
    var fdStart=event.target.id.indexOf("title_")
    if(fdStart == 0 && $(event.target).hasClass('dir')){
        $("#div_"+event.target.id.substr(6)).css("border", "3px dotted red");
    }
    //div被拖拽效果
    var fdStart=event.target.id.indexOf("div_")
    if(fdStart == 0 && $(event.target).hasClass('dir')){
        $("#"+event.target.id).css("border", "3px dotted red");
    }
    //ul被拖拽效果
    var fdStart=event.target.id.indexOf("ul_")
    if(fdStart == 0){
        $("#"+event.target.id).css("border", "3px dotted red");
    }
}
function dragLeave(event,obj){
    event.target.style.border = "";
    var fdStart=event.target.id.indexOf("title_")
    if(fdStart == 0){
        $("#div_"+event.target.id.substr(6)).css("border", "");
    }
}
function drop(event,obj) {
    event.preventDefault();
    event.stopPropagation();
    var data = event.dataTransfer.getData("target_id");
    //ul被拖拽效果
    var fdStart=event.target.id.indexOf("ul_")
    if(fdStart == 0){
        event.target.style.border = "";
        event.target.appendChild(document.getElementById(data));
        $.get('/notebook/note/change_dir/'+data+'/'+event.target.id,function(result){
                $(".main").html(result);
            });
    }

    //div被拖拽效果
    var fdStart=event.target.id.indexOf("div_")
    if(fdStart == 0 && $(event.target).hasClass('dir')){
        event.target.style.border = "";
        document.getElementById("ul_"+event.target.id.substr(4)).appendChild(document.getElementById(data));
        $.get('/notebook/note/change_dir/'+data+'/'+event.target.id,function(result){
                $(".main").html(result);
            });
    }
    //title被拖拽效果
    var fdStart=event.target.id.indexOf("title_")
    if(fdStart == 0 && $(event.target).hasClass('dir')){
        $("#div_"+event.target.id.substr(6)).css("border", "");
        document.getElementById("ul_"+event.target.id.substr(6)).appendChild(document.getElementById(data));
        $.get('/notebook/note/change_dir/'+data+'/'+event.target.id,function(result){
                $(".main").html(result);
            });
    }


}

