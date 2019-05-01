from Dent import *
#
b_stitch = Button(control, text="stitch and normalize", activeforeground="blue")
b_norms = Label(control, text="normalize takes about 10s", foreground="blue")
b_norms.grid(row=1, column=2)
b_stitch['command'] = lambda text=b_norms: stitch(b_norm = text)
b_stitch.grid(row=1, column=1)

# update button
t_norm = Label(control, text="crop take less than 1s", foreground="blue")
t_norm.grid(row=2, column=2)
b_norm = Button(control, text="crop", activeforeground="blue")
b_norm['command'] = lambda text=t_norm: raw.crop(t_norm = text)
b_norm.grid(row=2, column=1)

# update button
# slider
var = DoubleVar()
slider = Scale(control, variable=var, orient=HORIZONTAL, to=10, from_=200)
slider.set(110)
slider.grid(row=3, column=0)
# button
t_extract = Label(control, text="Extracting takes 2s", foreground="blue")
t_extract.grid(row=3, column=2)
b_extract = Button(control, text="extract", activeforeground="blue")
b_extract['command'] = lambda text=t_extract, slider=slider: raw.extract(t_extract = text, param= var.get())
b_extract.grid(row=3, column=1)

# update button
t_shift = Label(control, text="Shifting takes 4s", foreground="blue")
t_shift.grid(row=4, column=2)
b_shift = Button(control, text="shift", activeforeground="blue")
b_shift['command'] = lambda text=t_shift: raw.Shift(t_shift=text)
b_shift.grid(row=4, column=1)

# update button
# slider
var2 = DoubleVar()
slider2 = Scale(control, variable=var2, orient=HORIZONTAL, to=5, from_=30)
slider2.set(10)
slider2.grid(row=5, column=0)

t_cluster = Label(control, text="Clustering takes 7s", foreground="blue")
t_cluster.grid(row=5, column=2)
b_cluster = Button(control, text="cluster", activeforeground="blue")
b_cluster['command'] = lambda text=t_cluster, slider=slider2: raw.Cluster(t_cluster= text, param= var2.get())
b_cluster.grid(row=5, column=1)

# update button
t_label = Label(control, text="detecting takes 1s", foreground="blue")
t_label.grid(row=6, column=2)
b_detect = Button(control, text="detect", activeforeground="blue")
b_detect['command'] = lambda text=t_label: raw.Detection(t_detect=text, result=result)
b_detect.grid(row=6, column=1)

root.mainloop()