#!/usr/bin/ruby
class EjemploHilos
  def initialize
    @x = 0
  end

  def f1
    sleep 0.1
    print '+'
    @x += 3
  end

  def f2
    sleep 0.1
    print '*'
    @x *= 2
  end

  def run
    t1 = Thread.new {f1}
    t2 = Thread.new {f2}
    sleep 0.1
    print '%d ' % @x
  end
end

e = EjemploHilos.new
10.times { e.run }
