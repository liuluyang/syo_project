/**
 * Created by Administrator on 2019/1/3.
 */
var User = {
    mark: false, ErrorTime: 0, role: 0, Register: {
        InputFocus: function (type) {
            switch (type) {
                case 1:
                    if ($("#register_Name").val() == "邮箱") {
                        $("#register_Name").val("")
                    }
                    break;
                case 2:
                    $("#register_Pwd_Temp").hide();
                    $("#register_Pwd").show();
                    $("#register_Pwd").focus();
                    break;
                case 3:
                    if ($("#login_Name").val() == "邮箱") {
                        $("#login_Name").val("")
                    }
                    break;
                case 4:
                    $("#login_Pwd_Temp").hide();
                    $("#login_Pwd").show();
                    $("#login_Pwd").focus();
                    break;
                case 5:
                    $("#register_Pwd2_Temp").hide();
                    $("#register_qrPwd").show();
                    $("#register_qrPwd").focus();
                    break;
                default:
                    break
            }
        }, CheckInfo: function (type) {
            switch (type) {
                case 1:
                    var yxReg = /^[a-zA-Z0-9]+([._\\-]*[a-zA-Z0-9])*@([a-zA-Z0-9]+[-a-zA-Z0-9]*[a-zA-Z0-9]+.){1,63}[a-zA-Z0-9]+$/;
                    var sjhReg = /^1\d{10}$/;
                    if (!yxReg.test($("#register_Name").val()) && !sjhReg.test($("#register_Name").val())) {
                        $("#divNamePrompt").text("*账号格式错误,请输入注册时正确的邮箱");
                        $("#divNamePrompt").show();
                        User.mark = false
                    } else {
                        User.mark = true
                    }
                    break;
                case 2:
                    var pwd = $("#register_Pwd").val();
                    var pwd2 = $("#register_qrPwd").val() != "";
                    var yxReg = /^[a-zA-Z0-9_]{6,14}$/;
                    if (!yxReg.test(pwd)) {
                        $("#divPwd").show();
                        User.mark = false
                    } else {
                        $("#divPwdPrompt").hide();
                        if (pwd2 != "") {
                            if (pwd != pwd2) {
                                $("#twopwd").show();
                                User.mark = false
                            } else {
                                $("#twopwd").hide();
                                User.mark = true
                            }
                        } else {
                            User.mark = true
                        }
                    }
                    break;
                case 3:
                    var pwd = $("#register_Pwd").val();
                    var pwd2 = $("#register_qrPwd").val();
                    if (pwd != "" && pwd2 != "" && pwd == pwd2) {
                        $("#twopwd").hide();
                        User.mark = true
                    } else {
                        $("#twopwd").show();
                        User.mark = false
                    }
                    break;
                default:
                    break
            }
        }, Register: function () {
            User.Register.CheckInfo(1);
            User.Register.CheckInfo(2);
            User.Register.CheckInfo(3);
            if (!User.mark) {
                return false
            } else {
                if (!$("#chkUserDeal").attr("checked")) {
                    Lawyee.Tools.ShowMessage("您还未同意《用户协议》,无法完成注册！")
                } else {
                    var name = $("#register_Name").val();
                    var pwd = $("#register_Pwd").val();
                    $.post("/User/UserRegister", {
                        "UserName": name,
                        "Pwd": pwd,
                        "IsAdmin": 0
                    }, function (data) {
                        if (data == "1") {
                            $("#Register").hide();
                            $("#hn").val(name);
                            $("#RegisterSuccess").show()
                        } else {
                            if (data == "2") {
                                $("#divNamePrompt").text("*该账户已存在,请重新输入");
                                $("#divNamePrompt").show();
                                $("#hn").val("");
                                User.mark = false
                            } else {
                                $("#hn").val("");
                                Lawyee.Tools.ShowMessage(data)
                            }
                        }
                    })
                }
            }
        }, ShowLogin: function () {
            $("#Register").hide();
            $("#RegisterSuccess").hide();
            var name = $("#hn").val();
            $.post("/User/DirectLogin", {"name": name}, function (data) {
                top.window.location.href = "/index"
            })
        }
    }, Login: {
        RefreshValidateCode: function (obj) {
            obj.src = "/User/ValidateCode/" + Math.floor(Math.random() * 10000)
        }, CheckInfo: function (type) {
            if (type == "1") {
                if ($("#login_Name").val() == "" || $("#login_Name").val() == "邮箱") {
                    $("#divLogin_Name").show();
                    return false
                } else {
                    $("#divLogin_Name").hide()
                }
            }
            if (type == "2") {
                if ($("#login_Pwd").val() == "" || $("#login_Pwd").val() == "密码") {
                    $("#divLogin_Pwd").show();
                    return false
                } else {
                    $("#divLogin_Pwd").hide()
                }
            }
        }, SwitchRole: function (type) {
            if (type == 0) {
                $("#Login_User").attr("class", "login_role_common1 login_role_common3 float_left");
                $("#Login_Admin").attr("class", "login_role_common1 login_role_common2 float_right");
                $("#AutoLogin +span").show();
                $("#AutoLogin").show();
                User.role = 0
            } else {
                $("#Login_User").attr("class", "login_role_common1 login_role_common2 float_left");
                $("#Login_Admin").attr("class", "login_role_common1 login_role_common3 float_right");
                $("#AutoLogin +span").hide();
                $("#AutoLogin").hide();
                User.role = 1
            }
        }, Login: function (type) {
            if ($("#login_Name").val() == "" || $("#login_Name").val() == "邮箱") {
                $("#divLogin_Name").show();
                return false
            } else {
                $("#divLogin_Name").hide()
            }
            if ($("#login_Pwd").val() == "" || $("#login_Pwd").val() == "密码") {
                $("#divLogin_Pwd").show();
                return false
            } else {
                $("#divLogin_Pwd").hide()
            }
            if (User.ErrorTime >= 3) {
                if ($("#txtValidateCode").val() == "") {
                    Lawyee.Tools.ShowMessage("请输入验证码！");
                    return false
                }
            }
            var autoLogin = $("#AutoLogin").attr("checked") == true ? 1 : 0;
            $.post("/User/UserLogin", {
                "Role": User.role,
                "UserName": $("#login_Name").val(),
                "Pwd": $("#login_Pwd").val(),
                "ValidateCode": $("#txtValidateCode").val(),
                "ErrorTime": User.ErrorTime,
                "AutoLogin": autoLogin
            }, function (data) {
                if (data == "0") {
                    Lawyee.Tools.ShowMessage("验证码错误！")
                } else {
                    if (data == "2") {
                        Lawyee.Tools.ShowMessage("用户名或密码错误!");
                        User.ErrorTime++;
                        if (User.ErrorTime >= 3) {
                            $("#trValidateCode").show()
                        }
                    } else {
                        if (data == "1") {
                            if (User.role == 1) {
                                window.location.href = "/Admin/Admin"
                            } else {
                                if (type == 1) {
                                    var url = "";
                                    $.post("/User/GetUrl", function (datas) {
                                        url = datas;
                                        if (url == "") {
                                            window.history.go(-1)
                                        } else {
                                            if (url == "/") {
                                                top.window.location.href = "/index"
                                            } else {
                                                top.window.location.href = url
                                            }
                                        }
                                    })
                                }
                                window.location.href = "../Index"
                            }
                        } else {
                            Lawyee.Tools.ShowMessage(data)
                        }
                    }
                }
            })
        }, ChangeClick: function () {
            $("img[name='validateCode']").click()
        }
    }, ResetPwd: {
        Error: false, EmailCodeMark: 0, Step: function (type) {
            switch (type) {
                case 1:
                    User.ResetPwd.CheckUserName();
                    User.ResetPwd.CheckEmail(1);
                    User.ResetPwd.CheckValidateCode();
                    if (!User.ResetPwd.Error) {
                        return false
                    }
                    if (User.ResetPwd.Error) {
                        $.ajax({
                            type: "POST",
                            url: "/User/SendEmail",
                            data: {
                                "Email": $("#step1_Email").val(),
                                "ValidateCode": $("#ValidateCode").val()
                            },
                            async: false,
                            success: function (data) {
                                if (data == "1") {
                                    Lawyee.Tools.ShowMessage("邮件发送成功,请登录邮箱查看验证码！验证码1小时内有效！");
                                    $("#Email_Step2").text($("#step1_Email").val());
                                    $("#Step1").hide();
                                    $("#Step2").show();
                                    $("#txtEmailValidateCode").val("");
                                    $("#txtEmailValidateCode").focus();
                                    $("#ValidateCode_Step2").focus()
                                } else {
                                    Lawyee.Tools.ShowMessage(data)
                                }
                            }
                        })
                    }
                    break;
                case 2:
                    if (User.ResetPwd.EmailCodeMark == 3) {
                        $("#Step2").hide();
                        $("#Step3").show()
                    } else {
                        if ($("#txtEmailValidateCode").val() != "") {
                            Lawyee.Tools.ShowMessage("请先提交验证码！")
                        }
                    }
                    break;
                case 3:
                    if ($("#newPwd").val() != $("#confirmNewPwd").val() && $("#newPwd").val() != "") {
                        $("#divConfirmNewPwd").show();
                        return false
                    } else {
                        $("#divConfirmNewPwd").hide();
                        $.post("/User/ResetPwd", {
                            "Email": $("#Email_Step2").text(),
                            "Pwd": $("#confirmNewPwd").val()
                        }, function (data) {
                            if (data == "1") {
                                Lawyee.Tools.ShowMessage("密码重置成功！");
                                $("#Step3").hide();
                                $("#Step4").show()
                            } else {
                                Lawyee.Tools.ShowMessage(data)
                            }
                        })
                    }
                    break;
                default:
                    break
            }
        }, KeyPress: function (type) {
            if (event.keyCode == 13) {
                if (type == 1) {
                    User.ResetPwd.Step(1)
                }
                if (type == 2) {
                    User.ResetPwd.CheckEmailCode()
                }
            }
        }, CheckEmail: function (type) {
            var yxReg = /^[a-zA-Z0-9]+([._\\-]*[a-zA-Z0-9])*@([a-zA-Z0-9]+[-a-zA-Z0-9]*[a-zA-Z0-9]+.){1,63}[a-zA-Z0-9]+$/;
            if (type == 1) {
                if (!yxReg.test($("#step1_Email").val())) {
                    $("#step1_email").show();
                    User.ResetPwd.Error = false
                } else {
                    $("#step1_email").hide();
                    User.ResetPwd.Error = true
                }
            }
        }, CheckUserName: function () {
        }, CheckValidateCode: function () {
            if ($("#ValidateCode").val() == "") {
                $("#step1_validateCode").show();
                User.ResetPwd.Error = false
            } else {
                $("#step1_validateCode").hide();
                User.ResetPwd.Error = true
            }
        }, CheckPwd: function () {
            var pwdReg = /^[a-zA-Z0-9_]{6,14}$/;
            if (!pwdReg.test($("#newPwd").val())) {
                $("#divNewPwd").show();
                $("#newPwd").focus();
                Error = 1
            } else {
                $("#divNewPwd").hide()
            }
        }, CheckEmailInput: function () {
            if ($("#txtEmailValidateCode").val() == "") {
                $("#divEmailCode").show();
                User.ResetPwd.Error = false
            } else {
                $("#divEmailCode").hide();
                User.ResetPwd.Error = true
            }
        }, CheckEmailCode: function () {
            $.post("/User/CheckCode", {
                "Email": $("#Email_Step2").text(),
                "Code": $("#txtEmailValidateCode").val()
            }, function (data) {
                if (data == "1") {
                    User.ResetPwd.EmailCodeMark = 1;
                    Lawyee.Tools.ShowMessage("验证码已过期，返回上一步重新获取验证码!");
                    $("#Step2").hide();
                    $("#Step1").show();
                    $("#ValidateCode").val("");
                    $("#ChangeValidateCode").click()
                } else {
                    if (data == "2") {
                        User.ResetPwd.EmailCodeMark = 2;
                        Lawyee.Tools.ShowMessage("验证码错误，请重新输入验证码!");
                        $("#txtEmailValidateCode").val("");
                        $("#txtEmailValidateCode").focus()
                    } else {
                        User.ResetPwd.EmailCodeMark = 3;
                        Lawyee.Tools.ShowMessage("验证码正确!")
                    }
                }
            })
        }, CheckNewPwd: function () {
            if ($("#newPwd").val() != $("#confirmNewPwd").val() && $("#newPwd").val() != "") {
                $("#divConfirmNewPwd").show();
                return false
            } else {
                $("#divConfirmNewPwd").hide()
            }
        }, LoginAfterRegister: function () {
            window.location.href = "/User/RegisterAndLogin?Operate=1"
        }
    }, UserCenter: {
        SwitchTab: function (type) {
            if (type == 1) {
                $("#UserInfo").attr("class", "login_role_common1 login_role_common3 float_left");
                $("#AccountSetting").attr("class", "login_role_common1 login_role_common2 float_right");
                $("#accountSetting").hide();
                $("#personalInfo").show()
            } else {
                $("#UserInfo").attr("class", "login_role_common1 login_role_common2 float_left");
                $("#AccountSetting").attr("class", "login_role_common1 login_role_common3 float_right");
                $("#personalInfo").hide();
                $("#accountSetting").show()
            }
        }, SaveUserInfo: function () {
            var trueName = $("#TrueName").val();
            var sex = $("input[type='radio'][name='Sex']:checked").val();
            var birthday = $("#Birthday").val();
            var education = $("#Education").val();
            if (education.indexOf("请选择") > 0) {
                education = ""
            }
            var certificateType = $("input[type='radio'][name='CertificateType']:checked").val();
            var idNumber = $("#IDNumber").val();
            if (idNumber != "") {
                if (certificateType == "身份证") {
                    var regNumber = /^(\d{6})(18|19|20)?(\d{2})([01]\d)([0123]\d)(\d{3})(\d|X)?$/.test(idNumber);
                    var year = idNumber.substr(6, 4);
                    var month = idNumber.substr(10, 2);
                    var day = idNumber.substr(12, 2);
                    if (regNumber == false || month > 12 || day > 31) {
                        $("#IDNumber").val("");
                        Lawyee.Tools.ShowMessage("请输入正确的身份证号码！");
                        return
                    }
                }
                if (certificateType == "军官证") {
                    var regNumber = /南字第(\d{8})号|北字第(\d{8})号|沈字第(\d{8})号|兰字第(\d{8})号|成字第(\d{8})号|济字第(\d{8})号|广字第(\d{8})号|海字第(\d{8})号|空字第(\d{8})号|参字第(\d{8})号|政字第(\d{8})号|后字第(\d{8})号|装字第(\d{8})号/;
                    if (!regNumber.test(idNumber)) {
                        $("#IDNumber").val("");
                        Lawyee.Tools.ShowMessage("请输入正确的军官证号！");
                        return
                    }
                }
                if (certificateType == "护照") {
                    var regNumber = /(P\d{7})|(G\d{8})/;
                    if (!regNumber.test(idNumber)) {
                        $("#IDNumber").val("");
                        Lawyee.Tools.ShowMessage("请输入正确的护照号！");
                        return
                    }
                }
            }
            var telephone = $("#Telephone").val();
            if (telephone != "") {
                var mobile = /^[1][358][0-9]{9}$/;
                if (!mobile.test(telephone)) {
                    Lawyee.Tools.ShowMessage("手机号码不正确");
                    $("#Telephone").val("");
                    return
                }
            }
            var province = $("#4_container ul li[class='selected']").text();
            var city = $("#5_container ul li[class='selected']").text();
            var career = $("#7_container ul li[class='selected']").text();
            if (career.indexOf("请选择") > 0) {
                career = ""
            }
            var workUnit = $("#WorkUnit").val();
            var userInfo = "{ 'TrueName': '" + trueName + "','Sex': '" + sex + "','Birthday': '" + birthday + "','CertificateType': '" + certificateType + "','IDNumber': '" + idNumber + "','Telephone': '" + telephone + "','Education': '" + education + "','Province': '" + province + "','City': '" + city + "','Career': '" + career + "','WorkUnit': '" + workUnit + "','IsAdmin': '否' }";
            $.post("/User/SaveUserInfo", {"UserInfo": userInfo}, function (data) {
                if (data == "1") {
                    Lawyee.Tools.ShowMessage("保存成功!")
                } else {
                    if (data == "0") {
                        Lawyee.Tools.ShowMessage("保存失败!")
                    } else {
                        if (data == "2") {
                            Lawyee.Tools.ShowMessage("登录已过期，请重新登录!");
                            window.parent.document.location.href = "/User/RegisterAndLogin?Operate=1"
                        } else {
                            Lawyee.Tools.ShowMessage(data)
                        }
                    }
                }
            })
        }, ResetUserInfo: function () {
            $("#TrueName").val("");
            $("input[type='radio'][name='Sex']").eq(0).attr("checked", true);
            $("input[type='radio'][name='CertificateType']").eq(0).attr("checked", true);
            $("#Birthday").val("");
            $("select").find("option:first").attr("selected", "selected");
            $("select").render();
            $("#WorkUnit").val("");
            $("#IDNumber").val("");
            $("#Telephone").val("")
        }, ResetUserInfo: function () {
            $("#TrueName").val("");
            $("input[type='radio'][name='Sex']").eq(0).attr("checked", true);
            $("input[type='radio'][name='CertificateType']").eq(0).attr("checked", true);
            $("#Birthday").val("");
            $("select").find("option:first").attr("selected", "selected");
            $("select").render();
            $("#WorkUnit").val("");
            $("#IDNumber").val("");
            $("#Telephone").val("")
        }, FillUserInfo: function (pagenanme) {
            var userVal = $("#hidUserInfo").val();
            if (userVal != "") {
                if (pagenanme == "Edit") {
                    var userInfo = eval("(" + userVal + ")");
                    $("#UserName").text(userInfo.UserName);
                    $("#TrueName").val(userInfo.TrueName);
                    $("#Birthday").val(userInfo.Birthday);
                    $("input[type='radio'][value='" + userInfo.Sex + "']").attr("checked", "checked");
                    $("#Birthday").val(userInfo.Birthday);
                    $("input[type='radio'][value='" + userInfo.CertificateType + "']").attr("checked", "checked");
                    $("#Birthday").val(userInfo.Birthday);
                    $("#Education option[value='" + userInfo.Education + "']").attr("selected", "selected");
                    $("#Education").render();
                    $("#Province").attr("selectedvalue", userInfo.Province);
                    $("#City").attr("selectedvalue", userInfo.City);
                    $("#Career option[value='" + userInfo.Career + "']").attr("selected", "selected");
                    $("#Career").render();
                    $("#WorkUnit").val(userInfo.WorkUnit);
                    $("#IDNumber").val(userInfo.IDNumber);
                    $("#Telephone").val(userInfo.Telephone)
                } else {
                    var userInfo = eval("(" + userVal + ")");
                    $("#UserName").text(userInfo.UserName);
                    $("#TrueName").text(userInfo.TrueName);
                    $("#Telephone").text(userInfo.Telephone);
                    $("#Education").text(userInfo.Education == "0" ? "" : userInfo.Education);
                    var province = userInfo.Province;
                    var city = userInfo.City;
                    if (province != "" && city != "") {
                        province = province + " - "
                    }
                    $("#Province").text(province);
                    $("#City").text(city);
                    $("#Career").text(userInfo.Career);
                    $("#WorkUnit").text(userInfo.WorkUnit);
                    $("#AddTime").text(userInfo.AddTime)
                }
            }
        }, InputFocus: function (type) {
            switch (type) {
                case 1:
                    $("#original_Pwd_Temp").hide();
                    $("#original_Pwd").show();
                    $("#original_Pwd").focus();
                    break;
                case 2:
                    $("#new_Pwd_Temp").hide();
                    $("#new_Pwd").show();
                    $("#new_Pwd").focus();
                    break;
                default:
                    break
            }
        }, CheckInfo: function (type) {
            if (type == "1") {
                if ($("#original_Pwd").val() == "" || $("#original_Pwd").val() == "请输入原密码") {
                    $("#divOriginal_Pwd").show();
                    return false
                } else {
                    $("#divOriginal_Pwd").hide()
                }
            }
            if (type == "2") {
                if ($("#new_Pwd").val() == "") {
                    $("#divNew_Pwd").show();
                    return false
                } else {
                    $("#divNew_Pwd").hide()
                }
            }
            if (type == "3") {
                if ($("#confirm_Pwd").val() == "") {
                    $("#divConfirm_Pwd").text("请输入确认密码!");
                    $("#divConfirm_Pwd").show();
                    return false
                } else {
                    if ($("#new_Pwd").val() != $("#confirm_Pwd").val()) {
                        $("#divConfirm_Pwd").text("两次输入的密码不一致!");
                        $("#divConfirm_Pwd").show();
                        return false
                    } else {
                        $("#divConfirm_Pwd").hide()
                    }
                }
            }
        }, ChangePwd: function () {
            var newPwd = $("#new_Pwd").val();
            var confirmPwd = $("#confirm_Pwd").val();
            if (newPwd.length < 6 || confirmPwd.length < 6) {
                alert("新密码长度不得小于6位");
                return
            }
            if (newPwd != "" && (newPwd == confirmPwd)) {
                $.post("/User/ChangeUserPassword", {
                    "originalPwd": $("#original_Pwd").val(),
                    "newPwd": $("#new_Pwd").val()
                }, function (data) {
                    if (data == "1") {
                        Lawyee.Tools.ShowMessage("修改成功!");
                        window.parent.document.location.href = window.parent.document.location.href
                    } else {
                        if (data == "0") {
                            Lawyee.Tools.ShowMessage("登录已过期，请重新登录!");
                            window.parent.document.location.href = "/User/RegisterAndLogin?Operate=1"
                        } else {
                            Lawyee.Tools.ShowMessage("原密码错误，请重新输入！")
                        }
                    }
                })
            }
        }, Reset: function () {
            $("#original_Pwd").val("");
            $("#new_Pwd").val("");
            $("#confirm_Pwd").val("")
        }
    }
};