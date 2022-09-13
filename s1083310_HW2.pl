#!/usr/bin/perl -w
use strict;

# label and image production
sub preprocess {
  # make files
  my $Max_Num;
  my $path;
  my @files;
  my $EC;
  my @pssm;
  my %dic;
  ($Max_Num, $path, @files)= @_;
  
  for(1..(scalar(@files) - 1))
  {
    #find EC number
    $files[$_] = '>' . $files[$_];
    $files[$_] =~ />(\S+):(\d+)./ and $EC = $2;
  
    if (defined ($dic{$EC})) {
      if ($dic{$EC} >= $Max_Num)
      {
        next;
      }
    }
    
    #image production
    open(FH,'>',"$path/image/convert.fa") or die $!;
    print FH $files[$_];
    close(FH);
    
    #pssm productuin
    `bin/psiblast -db uniprot.fasta -query $path/image/convert.fa -out outfile -outfmt 6 -save_pssm_after_last_round -out_ascii_pssm "$path/image/convert.pssm"`;
    
    #cut the pssm
    @pssm = split /\n/, `cat "$path/image/convert.pssm"`;
    my $start = index($pssm[2], "A") - 1;
    my $end = index($pssm[2], "V") + 1;
    my $length = $end - $start;
    @pssm = @pssm[3..(scalar(@pssm) - 7)];
    for(0..(scalar(@pssm) - 1))
    {
      $pssm[$_] = substr($pssm[$_], $start, $length) . "\n";
    }
    @pssm = @pssm[3..(scalar(@pssm) - 7)];
    
    if (scalar(@pssm) >= 100)
    {
      if (defined ($dic{$EC})) 
      {
        $dic{$EC} += 1;
      }
      else
      {
        $dic{$EC} = 1;
      }
      
      @pssm = @pssm[0..99];
      #answer production
      open(FH,'>',"$path/label/$_.txt") or die $!;
      print FH $EC;
      close(FH);
      
      #save the pssm
      open(FH,'>',"$path/image/$_.pssm") or die $!;
      print FH @pssm;
      close(FH);
    }
    
    foreach my $key(keys %dic) # key-value pair
    {
        print "key:$key,value:$dic{$key}\n";
    }
    print "\n";
  }
  `rm -f "$path/image/convert.fa"`;
  `rm -f "$path/image/convert.pssm"`;
}

my $fn = shift; # argument
my @train = split />/, `cat $fn`;
$fn = shift; # argument
my @test = split />/, `cat $fn`;

(-e "/train") or `mkdir -p train/image train/label train/text`;
(-e "/test") or `mkdir -p test/image test/label test/text`;

&preprocess(100, "train", @train);
&preprocess(20, "test", @test);

`Rscript s1083310_HW2.r`;

`python3.7 s1083310_HW2.py`;
print("The result is in model_result.txt")