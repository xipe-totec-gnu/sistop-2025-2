	.file	"ilustrando_loc_ref.c"
	.text
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"El valor final de a es: %d\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB11:
	.cfi_startproc
	movl	$2, %esi
	movl	$100, %eax
	.p2align 3
	.p2align 4
	.p2align 3
.L2:
	sall	$2, %esi
	subl	$2, %eax
	jne	.L2
	leaq	.LC0(%rip), %rdi
	xorl	%eax, %eax
	jmp	printf@PLT
	.cfi_endproc
.LFE11:
	.size	main, .-main
	.ident	"GCC: (Debian 14.2.0-18) 14.2.0"
	.section	.note.GNU-stack,"",@progbits
