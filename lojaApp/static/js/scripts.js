const galleryImages = document.querySelectorAll('.gallery-image');
const imageModal = document.getElementById('imageModal');
const modalImage = document.getElementById('modalImage');
const closeModalButton = document.getElementById('closeModal');

if (imageModal && modalImage && closeModalButton) {
	let lastFocusedImage = null;

	const openModal = (image) => {
		lastFocusedImage = image;
		modalImage.src = image.currentSrc || image.src;
		modalImage.alt = image.alt;
		imageModal.classList.add('active');
		imageModal.setAttribute('aria-hidden', 'false');
		closeModalButton.focus();
	};

	const closeModal = () => {
		imageModal.classList.remove('active');
		imageModal.setAttribute('aria-hidden', 'true');
		modalImage.removeAttribute('src');
		if (lastFocusedImage) {
			lastFocusedImage.focus();
		}
	};

	galleryImages.forEach((image) => {
		image.addEventListener('click', () => openModal(image));
		image.addEventListener('keydown', (event) => {
			if (event.key === 'Enter' || event.key === ' ') {
				event.preventDefault();
				openModal(image);
			}
		});
	});

	closeModalButton.addEventListener('click', closeModal);
	imageModal.addEventListener('click', (event) => {
		if (event.target === imageModal) {
			closeModal();
		}
	});
	document.addEventListener('keydown', (event) => {
		if (event.key === 'Escape' && imageModal.classList.contains('active')) {
			closeModal();
		}
	});
}
