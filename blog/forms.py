#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/6

from django import forms
from django.core.exceptions import ValidationError
from blog import models

class RegisterForm(forms.Form):

    username = forms.CharField(min_length=4,
                               max_length=12,
                               widget=forms.TextInput(attrs={"class":"form-control","placeholder":"username"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"password"}))

    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"repeat_password"}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"email"}))

    valid_code = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"valid_code"}))

    def __init__(self,request,*args,**kwargs):

        super(RegisterForm,self).__init__(*args,**kwargs)
        self.request=request


    def clean_password(self):
        '''
        密码钩子
        :return: 
        '''

        if len(self.cleaned_data["password"])>=8:
            return self.cleaned_data["password"]
        else:
            raise ValidationError("密码小于8位！")

    def clean_username(self):
        '''
        用户名钩子
        :return: 
        '''
        if models.UserInfo.objects.filter(username=self.cleaned_data["username"]):
            raise ValidationError("用户名已存在！")
        elif self.cleaned_data["username"].isdigit() or self.cleaned_data["username"].isalpha():
            raise ValidationError("用户名必须包含数字与字母！")
        else:
            return self.cleaned_data["username"]

    def clean_valid_code(self):
        '''
        验证码钩子
        :return: 
        '''
        if self.cleaned_data.get("valid_code").upper() == self.request.session.get("valid_code").upper():
            return self.cleaned_data["valid_code"]


        else:
            raise ValidationError("验证码输入错误！")


    def clean(self):
        '''
        全局钩子
        :return: 
        '''
        if self.cleaned_data.get("password",0)==self.cleaned_data.get("repeat_password",1):

            return self.cleaned_data
        else:
            raise ValidationError("密码不一致")


























