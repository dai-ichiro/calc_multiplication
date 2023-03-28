from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QSlider

import yaml

def construct(x, yaml_file, settings):

    with open(yaml_file, 'r') as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

    if settings in yaml_data.keys():

        settings_dict = yaml_data[settings]

        if settings_dict['type'] == 'QLabel':
            
            ##サイズの設定
            if ('height' in settings_dict.keys() and 'width' in settings_dict.keys()):

                h = settings_dict['height']
                w = settings_dict['width']

                x.setFixedSize(QSize(w, h))
            ##サイズの設定

            ##fontの設定
            font = QFont()

            if 'fontFamily' in settings_dict.keys():
                font.setFamily(settings_dict['fontFamily'])

            if 'fontPoint' in settings_dict.keys():
                font.setPointSize(settings_dict['fontPoint'])

            if 'fontBold' in settings_dict.keys():
                font.setBold(settings_dict['fontBold'])
                    
            x.setFont(font)
            ##fontの設定

            ##テキストの設定
            if 'text' in settings_dict.keys():
                x.setText(settings_dict['text'])
            ##テキストの設定

            ##アライメントの設定
            if 'alignment' in settings_dict.keys():

                alignment_str = settings_dict['alignment']

                if alignment_str == 'center':
                    x.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                elif alignment_str == 'right':
                    x.setAlignment(Qt.AlignmentFlag.AlignRight)

                elif alignment_str == 'left':
                    x.setAlignment(Qt.AlignmentFlag.AlignLeft)
            ##アライメントの設定

            ##枠線の設定（線の太さ)
            if 'linewidth' in settings_dict.keys():
                x.setLineWidth(settings_dict['linewidth'])
            ##枠線の設定（線の太さ)

            ##枠線の設定（ボックスタイプと影）
            if ('shape' in settings_dict.keys() and 'shadow' in settings_dict.keys()):

                if settings_dict['shape'] == 'box':

                    if settings_dict['shadow'] == 'plain':
                        x.setFrameStyle(QFrame.Shape.Box.value | QFrame.Shadow.Plain.value)
                    
                    elif settings_dict['shadow'] == 'raised':
                        x.setFrameStyle(QFrame.Shape.Box.value | QFrame.Shadow.Raised.value)

                    elif settings_dict['shadow'] == 'sunken':
                        x.setFrameStyle(QFrame.Shape.Box.value | QFrame.Shadow.Sunken.value)

                elif settings_dict['shape'] == 'panel':

                    if settings_dict['shadow'] == 'plain':
                        x.setFrameStyle(QFrame.Shape.Panel.value | QFrame.Shadow.Plain.value)
                    
                    elif settings_dict['shadow'] == 'raised':
                        x.setFrameStyle(QFrame.Shape.Panel.value | QFrame.Shadow.Raised.value)

                    elif settings_dict['shadow'] == 'sunken':
                        x.setFrameStyle(QFrame.Shape.Panel.value | QFrame.Shadow.Sunken.value)
            ##枠線の設定（ボックスタイプと影）

            ##色の設定
            color_list = []
            if 'color' in settings_dict.keys():
                color_list.append('color: %s'%settings_dict['color'])
            if 'background-color' in settings_dict.keys():
                color_list.append('background-color: %s'%settings_dict['background-color'])

            if len(color_list) > 0:
                x.setStyleSheet(';'.join(color_list))
            ##色の設定

        elif settings_dict['type'] == 'QPushButton':
            
            ##サイズの設定
            if ('height' in settings_dict.keys() and 'width' in settings_dict.keys()):

                h = settings_dict['height']
                w = settings_dict['width']

                x.setFixedSize(QSize(w, h))
            ##サイズの設定

            ##fontの設定
            font = QFont()

            if 'fontFamily' in settings_dict.keys():
                font.setFamily(settings_dict['fontFamily'])

            if 'fontPoint' in settings_dict.keys():
                font.setPointSize(settings_dict['fontPoint'])

            if 'fontBold' in settings_dict.keys():
                font.setBold(settings_dict['fontBold'])
                    
            x.setFont(font)
            ##fontの設定

            ##テキストの設定
            if 'text' in settings_dict.keys():
                x.setText(settings_dict['text'])
            ##テキストの設定
        
        elif settings_dict['type'] == 'QSlider':

            ##サイズの設定
            if ('height' in settings_dict.keys() and 'width' in settings_dict.keys()):

                h = settings_dict['height']
                w = settings_dict['width']

                x.setFixedSize(QSize(w, h))
            ##サイズの設定
            
            ##オリエンテーションの設定
            if 'orientation' in settings_dict.keys():

                orientation_type = settings_dict['orientation']

                if orientation_type == 'h':
                    x.setOrientation(Qt.Orientation.Horizontal)
                
                elif orientation_type == 'v':
                    x.setOrientation(Qt.Orientation.Vertical)
            ##オリエンテーションの設定

            ##値の設定
            if 'max' in settings_dict.keys():
                x.setMaximum(settings_dict['max'])
            
            if 'min' in settings_dict.keys():
                x.setMinimum(settings_dict['min'])

            if 'default' in settings_dict.keys():
                x.setValue(settings_dict['default'])
            ##値の設定

            ##目盛りの設定
            if 'tickposition' in settings_dict.keys():
                tickposition = settings_dict['tickposition']

                if tickposition == 'both':
                    x.setTickPosition(QSlider.TickPosition.TicksBothSides)
                
                elif tickposition == 'above':
                    x.setTickPosition(QSlider.TickPosition.TicksAbove)
                
                elif tickposition == 'below':
                    x.setTickPosition(QSlider.TickPosition.TicksBelow)

                elif tickposition == 'left':
                    x.setTickPosition(QSlider.TickPosition.TicksLeft)
                
                elif tickposition == 'right':
                    x.setTickPosition(QSlider.TickPosition.TicksRight)
            ##目盛りの設定

    return x