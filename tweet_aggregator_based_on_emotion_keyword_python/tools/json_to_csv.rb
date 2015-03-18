require 'rubygems'
require 'json'
require 'csv'
require 'ruby-debug'

fin = ARGV[0]
puts "Loading...\t#{fin}"

file = File.open(fin, 'r')
json = file.readlines.to_s
hash = JSON.parse(json)

debugger

fout = ARGV[0] + ".txt"
fo = File.open(fout, 'w')

#my_twitter_handle = /\s@.+\s?/i
twitter_handle = /@([A-Za-z0-9_]+)/

hash.each do |k,v|
#	fo << (k + "\n") # for filter_words

	cleaned_str = v.gsub(twitter_handle, '@XXX').strip
	cleaned_str = cleaned_str.gsub(/[\n\r]/,'')

	fo << ( cleaned_str + "\n" ) #('"'+ cleaned_str + '",')

end

#CSV.open(fout, 'w') do |csv|
#  JSON.parse(File.open("foo.json").read).each do |hash|
#    csv << hash.values
#  end
#end


fo.close
puts 'end of program'
