#!/usr/bin/env ruby
#Copyright (C) 2015 Lisong Wang <lswang@ibcas.ac.cn>
#Distributed under terms of the GNU GPL 3 license.
#encoding: utf-8
#parse KML file place to txt file


require 'nokogiri'

# user provide data file
from_file, to_file, file_province = ARGV


prompt = '>'

puts "please provide your input file name:", prompt
from_file = $stdin.gets.chomp

puts "please provide your output file name:", prompt
to_file = $stdin.gets.chomp

puts "please provide provice or region name for the moutain kml file", prompt
file_province = $stdin.gets.chomp

# read data into nokogir object by kml file input
#
@xml_doc = Nokogiri::XML(File.open(from_file))
head  = "Province, Name, Latitude, Longitude" + "\n"

f = File.open(to_file, "w")
f << head

@xml_doc.css('Placemark').each do |placemark|
  mountain_names = placemark.css('name')
  coordinates = placemark.css('coordinates')

  if file_province && mountain_names && coordinates
    coordinates.text.split(" ").each do |coordinate|
      lon = coordinate.split(',')[0]
      lat = coordinate.split(',')[1]
      f << file_province + "," + mountain_names.text + "," + lat + "," + lon + "\n"
    end
  end
end

f.close
