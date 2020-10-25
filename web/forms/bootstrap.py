class BootStrap(object):
    bootstrap_class_exclude=[]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,filed in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue
            if name in self.bootstrap_class_exclude:
                continue
            old_class = filed.widget.attrs.get('class', "")
            filed.widget.attrs['class'] = '{} form-control'.format(old_class)
            filed.widget.attrs['placeholder']='请输入'+filed.label