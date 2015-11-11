CUET
====

根据cue裁剪专辑

### USAGE

`./main cue_filename.cue [out_dir]`

裁剪音频文件依赖[PyAV](https://github.com/mikeboers/PyAV)

如果没有PyAV也能获取cue信息

*参考`Cuet.py`*

### REQUIREMENTS

- pyav
    ```
    on MAC

    brew install ffmpeg pkg-config
    pip install av
    ```
