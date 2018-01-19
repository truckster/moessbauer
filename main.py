import steel, eisensulfat, weicheisen

input_path = "/home/gpu/Documents/Praktikum/WS1718/Gruppe2/"
weicheisen_filename = "weicheisen.txt"
weicheisen_cassy = "Aufg2Weicheisen.txt"
steel_filename = "stahl.txt"
steel_cassy = "Aufg2Stahl.txt"
eisensulfat_filename = "eisensulfat.txt"
eisensulfat_cassy = "Aufg2Eisensulfat.txt"

# weicheisen.read_manual_file(input_path, weicheisen_filename)
# steel.read_manual_file(input_path, steel_filename)
# eisensulfat.read_manual_file(input_path, eisensulfat_filename)

channels, counts = weicheisen.read_cassy_file(input_path, weicheisen_cassy)
weicheisen.fit_it(channels, counts, input_path)

channels, counts = steel.read_cassy_file(input_path, steel_cassy)
steel.fit_it(channels, counts, input_path)

channels, counts = eisensulfat.read_cassy_file(input_path, eisensulfat_cassy)
eisensulfat.fit_it(channels, counts, input_path)


