class BootstrapForm(object):
    # 为所有标签加上样式
    def __init__(self, *args, **kwargs):
        bootstrap_class_exclude = []
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{0}'.format(field.label)
